#!/usr/bin/env python3
"""Loopback-only photography assistant; provider keys live only in server memory."""
import argparse
import getpass
import importlib.util
import json
import os
import secrets
import re
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('rag', ROOT/'scripts/ask-photography.py')
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)
WEB = Path(__file__).resolve().parent/'web'


def public_result(result):
    """Never forward diagnostic drafts, usage, keys or project annotations to visitors."""
    return {k: result[k] for k in ('status', 'answer', 'evidence_notice', 'setup_context', 'citation_check', 'answer_method', 'validation_failures') if k in result} | {
        'passages': [{k: p.get(k) for k in ('source_id', 'text', 'url', 'section', 'representation')} for p in result.get('passages', [])]
    }


class AppServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, query=None, public_host=None):
        super().__init__(address, Handler)
        self.query = query
        self.public_host = public_host
        self.csrf = secrets.token_urlsafe(32)
        self.active = threading.BoundedSemaphore(1)
        self.requests = deque()
        self.rate_lock = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # No question text, keys or request logs persisted.

    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def send(self, status, body, mime='application/json; charset=utf-8'):
        raw = json.dumps(body, ensure_ascii=False).encode() if isinstance(body, dict) else body
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        self.end_headers()
        self.wfile.write(raw)

    def valid_host(self):
        allowed = {self.server.public_host} if self.server.public_host else {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        return self.headers.get('Host') in allowed

    def do_GET(self):
        if self.path == '/healthz':
            return self.send(200, {'status': 'ok', 'mode': 'live' if self.server.query else 'preview'})
        if not self.valid_host():
            return self.send(403, {'error': 'Host not allowed.'})
        if self.path == '/api/config':
            return self.send(200, {'mode': 'live' if self.server.query else 'preview', 'token': self.server.csrf, 'answer_method': 'source_checklist_v1', 'expanded': rag.active_collection() == 'photography_expanded_v1'})
        files = {'/': ('index.html', 'text/html; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'), '/style.css': ('style.css', 'text/css; charset=utf-8')}
        if self.path not in files:
            return self.send(404, {'error': 'Page not found.'})
        name, mime = files[self.path]
        return self.send(200, (WEB/name).read_bytes(), mime)

    def do_POST(self):
        host = self.headers.get('Host', '')
        expected_origin = ('https://' if self.server.public_host else 'http://')+host
        if not self.valid_host() or self.headers.get('Origin') != expected_origin or self.headers.get('X-App-Token') != self.server.csrf:
            return self.send(403, {'error': 'Reload this app and try again.'})
        if self.path not in ('/api/ask', '/api/example'):
            return self.send(404, {'error': 'Endpoint not found.'})
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.send(415, {'error': 'Use a JSON request.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 8000:
                return self.send(413, {'error': 'Request is too large or empty.'})
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError()
        except (ValueError, TimeoutError):
            return self.send(400, {'error': 'Invalid request.'})
        if self.path == '/api/example':
            case = body.get('case')
            if case not in ('E1', 'E3', 'E5'):
                return self.send(400, {'error': 'Choose one of the saved examples.'})
            data = json.loads((ROOT/'docs/public/photography-evaluation-round-3.json').read_text())
            item = next(c for c in data['cases'] if c['case'] == case)
            result = public_result(item['result'])
            if result['status'] != 'generated':
                result['status'] = 'insufficient_evidence'
                result['answer'] = 'The available source does not contain enough evidence to answer this question. Try a question about tripod-based night-sky photography.'
            return self.send(200, {'question': item['question'], 'mode': 'saved_example', **result})
        question = body.get('question')
        if not isinstance(question, str) or not 1 <= len(question.strip()) <= 1000:
            return self.send(400, {'error': 'Write a question between 1 and 1,000 characters.'})
        if not self.server.query:
            return self.send(503, {'error': 'Live answers are not connected in this preview. Choose a saved example to explore the interface.'})
        if not self.server.active.acquire(blocking=False):
            return self.send(429, {'error': 'Another question is being answered. Please try again shortly.'})
        try:
            now = time.monotonic()
            with self.server.rate_lock:
                while self.server.requests and now-self.server.requests[0] >= 60:
                    self.server.requests.popleft()
                if len(self.server.requests) >= 3:
                    return self.send(429, {'error': 'Please wait a minute. This prototype allows three questions per minute.'})
                self.server.requests.append(now)
            result = public_result(self.server.query(question.strip()))
            return self.send(200, {'question': question.strip(), 'mode': 'live', **result})
        except HTTPError as error:
            message = 'The provider limit was reached. Please try again later.' if error.code == 429 else 'The answer service could not complete this request. Check the server connection and try again.'
            return self.send(503, {'error': message})
        except (URLError, TimeoutError, rag.ResponseError, ValueError, KeyError, TypeError, IndexError):
            return self.send(503, {'error': 'The answer service is temporarily unavailable. No answer was generated.'})
        finally:
            self.server.active.release()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Prompt privately for keys and enable actual Qdrant/Groq requests')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--bind', choices=['127.0.0.1', '0.0.0.0'], default='127.0.0.1')
    parser.add_argument('--public-host', help='Exact HTTPS hostname, for deployment behind the existing proxy')
    parser.add_argument('--noninteractive', action='store_true', help='Fail if server-side credential files are missing')
    args = parser.parse_args()
    if args.public_host and not re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)*\.[a-z]{2,}', args.public_host):
        parser.error('Use a plain lowercase DNS hostname.')
    if args.bind == '0.0.0.0' and not args.public_host:
        parser.error('A public hostname is required for container binding.')
    query = None
    if args.live:
        print('Keys stay in server memory. Questions go to Qdrant; retrieved evidence and questions go to Groq.')
        try:
            def load_key(name, label):
                value = os.environ.get(name)
                key_file = os.environ.get(name+'_FILE')
                if not value and key_file:
                    try:
                        value = Path(key_file).read_text()
                    except OSError:
                        raise ValueError(label+' credential file is missing or unreadable.') from None
                if not value and not args.noninteractive:
                    value = getpass.getpass(label+' API key (hidden): ')
                return rag.clean_key(value or '', label)
            qkey = load_key('QDRANT_API_KEY', 'Qdrant')
            gkey = load_key('GROQ_API_KEY', 'Groq')
        except ValueError as error:
            parser.error(str(error))
        def query(question):
            # Reload only this local, developer-owned pipeline file between requests.
            # Credentials remain in the closure and never touch disk or the browser.
            pipeline_spec = importlib.util.spec_from_file_location('rag_live', ROOT/'scripts/ask-photography.py')
            pipeline = importlib.util.module_from_spec(pipeline_spec)
            pipeline_spec.loader.exec_module(pipeline)
            try:
                return pipeline.answer(question, qkey, gkey, real=True)
            except pipeline.ResponseError as error:
                raise rag.ResponseError(str(error)) from None
    server = AppServer((args.bind, args.port), query, args.public_host)
    print(f'Photography assistant ({"live" if query else "saved-example preview"}): http://127.0.0.1:{server.server_port}', flush=True)
    print('Keep this terminal open. Ctrl+C stops the app. No keys or questions are saved.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
