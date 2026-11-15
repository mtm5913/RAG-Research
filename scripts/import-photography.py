#!/usr/bin/env python3
"""Import the reviewed NPS prose pilot into a separate Qdrant collection."""
import getpass
import importlib.util
import json
from pathlib import Path
from urllib.error import HTTPError, URLError

root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('rag', root/'scripts/ask-photography.py')
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)
source = json.loads((root/'corpus/photography-pilot.json').read_text())
print('Imports three NPS prose paraphrases into photography_pilot_v1. Does not change photography_smoke_test.')
key = getpass.getpass('Qdrant API key (hidden): ').strip()
if not key:
    raise SystemExit('No key entered.')
url = rag.DEFAULT_URL+'/collections/photography_pilot_v1'

def put(endpoint, body):
    import ssl, sys
    from urllib.request import Request, urlopen
    context = ssl.create_default_context(cafile='/etc/ssl/cert.pem') if sys.platform == 'darwin' else ssl.create_default_context()
    req = Request(endpoint, data=json.dumps(body).encode(), headers={'api-key': key, 'Content-Type': 'application/json', 'User-Agent': 'PhotographyResearchApp/0.1'}, method='PUT')
    with urlopen(req, timeout=60, context=context) as response:
        return json.load(response)

try:
    # Qdrant refuses an existing name; never recreate or delete a collection.
    try:
        created = put(url, {'vectors': {'size': 384, 'distance': 'Cosine'}})
        print(json.dumps({'create_status': created.get('status')}))
    except HTTPError as error:
        if error.code != 409:
            raise
        print('Collection already exists; check its vector configuration before a repeat import. Stopping without changes.')
        raise SystemExit(1)
    points = []
    for chunk in source['chunks']:
        points.append({'id': chunk['id'], 'vector': {'text': chunk['text'], 'model': 'sentence-transformers/all-MiniLM-L6-v2'}, 'payload': {
            'source_id': chunk['source_id'], 'document_id': source['document_id'], 'title': source['title'], 'url': source['url'],
            'section': chunk['section'], 'text': chunk['text'], 'synthetic': False, 'representation': source['representation'],
            'accessed': source['accessed'], 'permission_url': source['permission_url']}})
    result = put(url+'/points?wait=true', {'points': points})
    print(json.dumps({'import_status': result.get('status'), 'result': result.get('result'), 'passages': len(points)}))
except HTTPError as error:
    raise SystemExit('Qdrant rejected request: HTTP '+str(error.code)+'. No key printed.')
except (URLError, TimeoutError):
    raise SystemExit('Connection failed or timed out. Collection may be empty if creation succeeded; no import success claimed. No key printed.')
