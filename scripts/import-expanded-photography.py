#!/usr/bin/env python3
"""Import the reviewed two-source collection, then activate it locally. No key is saved."""
import getpass
import importlib.util
import json
import ssl
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('rag',ROOT/'scripts/ask-photography.py')
rag=importlib.util.module_from_spec(spec);spec.loader.exec_module(rag)
bundle=json.loads((ROOT/'corpus/photography-expanded.json').read_text())
collection='photography_expanded_v1'
assert bundle['collection']==collection
print('Imports 7 checked paraphrase passages from 2 NPS sources into a separate collection.')
print('Leaves the original pilot and synthetic collections intact. Activates the expanded collection only after verification.')
key=rag.clean_key(getpass.getpass('Qdrant API key (hidden): '),'Qdrant')
context=ssl.create_default_context(cafile='/etc/ssl/cert.pem') if sys.platform=='darwin' else ssl.create_default_context()
url=rag.DEFAULT_URL+'/collections/'+collection

def call(method,endpoint,body=None):
 req=Request(endpoint,data=json.dumps(body).encode() if body is not None else None,headers={'api-key':key,'Content-Type':'application/json','User-Agent':'PhotographyResearchApp/0.1'},method=method)
 with urlopen(req,context=context,timeout=60) as response:return json.load(response)
try:
 try:
  call('PUT',url,{'vectors':{'size':384,'distance':'Cosine'}})
 except HTTPError as error:
  if error.code!=409:raise
  config=call('GET',url)['result']['config']['params']['vectors']
  if config.get('size')!=384 or config.get('distance')!='Cosine':raise SystemExit('Existing expanded collection has incompatible vectors. No import attempted.')
 points=[]
 for doc in bundle['documents']:
  for chunk in doc['chunks']:
   points.append({'id':chunk['id'],'vector':{'text':chunk['text'],'model':'sentence-transformers/all-MiniLM-L6-v2'},'payload':{
    'source_id':chunk['source_id'],'document_id':doc['document_id'],'title':doc['title'],'url':doc['url'],'section':chunk['section'],'text':chunk['text'],
    'synthetic':False,'representation':doc['representation'],'permission_url':doc['permission_url'],'accessed':doc['accessed']}})
 # Original pilot IDs are 1–3, additions 4–7; no duplicate IDs are allowed.
 assert len(points)==7 and len({p['id'] for p in points})==7
 result=call('PUT',url+'/points?wait=true',{'points':points})
 if result.get('status')!='ok' or result.get('result',{}).get('status')!='completed':raise SystemExit('Import not confirmed complete. Existing active collection remains unchanged.')
 count=call('POST',url+'/points/count',{'exact':True})['result']['count']
 if count!=7:raise SystemExit('Unexpected point count. Existing active collection remains unchanged.')
 activation=ROOT/'.local-corpus.json'
 temporary=ROOT/'.local-corpus.json.tmp'
 temporary.write_text(json.dumps({'collection':collection,'documents':2,'passages':count}))
 temporary.replace(activation)
 print(json.dumps({'status':'ok','collection':collection,'documents':2,'passages':count,'activated_locally':True,'restart_required':False}))
except HTTPError as error:raise SystemExit('Qdrant rejected request: HTTP '+str(error.code)+'. No key printed; activation not confirmed.')
except (URLError,TimeoutError,ValueError,KeyError,TypeError):raise SystemExit('Connection or response verification failed. No key printed; activation not confirmed.')
