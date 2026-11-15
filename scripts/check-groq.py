#!/usr/bin/env python3
"""One synthetic Groq API grounding check. Prompts privately; never saves the key."""
import getpass
import json
import sys
import ssl
import socket
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

key = getpass.getpass('Groq API key (hidden; sent only to api.groq.com): ').strip()
if not key:
    sys.exit('No key entered.')
payload = {
    'model': 'openai/gpt-oss-120b',
    'messages': [
        {'role': 'system', 'content': 'Use only the supplied evidence. Never invent camera settings. If evidence is insufficient, say so explicitly. Cite the passage ID. Keep the final answer under 120 words.'},
        {'role': 'user', 'content': 'Synthetic evidence [SYNTHETIC-01]: Synthetic test passage about photographing stars at night with a camera on a tripod.\nQuestion: What exact aperture, shutter speed and ISO should I use on a Canon EOS R1 for a starry sky?'}
    ],
    'max_completion_tokens': 800,
    'temperature': 0
}
request = Request('https://api.groq.com/openai/v1/chat/completions', data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer '+key, 'Content-Type': 'application/json', 'User-Agent': 'PhotographyResearchApp/0.1'}, method='POST')
context = ssl.create_default_context()
if sys.platform == 'darwin' and Path('/etc/ssl/cert.pem').is_file():
    context = ssl.create_default_context(cafile='/etc/ssl/cert.pem')
try:
    with urlopen(request, timeout=60, context=context) as response:
        result = json.load(response)
        print(json.dumps({'http_status': response.status, 'model': result.get('model'), 'answer': result['choices'][0]['message'].get('content'), 'finish_reason': result['choices'][0].get('finish_reason'), 'usage': result.get('usage')}, indent=2))
except HTTPError as error:
    print('Groq request rejected: HTTP '+str(error.code)+'. No key printed.', file=sys.stderr)
    sys.exit(1)
except URLError as error:
    if isinstance(error.reason, ssl.SSLCertVerificationError):
        sys.exit('Certificate verification failed. No key printed.')
    if isinstance(error.reason, socket.gaierror):
        sys.exit('DNS lookup failed. Check your network. No key printed.')
    sys.exit('Network connection failed ('+type(error.reason).__name__+'). No key printed.')
except TimeoutError:
    sys.exit('Request timed out after 60 seconds. No key printed.')
