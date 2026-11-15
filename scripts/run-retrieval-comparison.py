#!/usr/bin/env python3
"""Compare a local keyword baseline with observed public-app retrieval; no API keys."""
import hashlib
import importlib.util
import json
import ssl
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('baseline',ROOT/'scripts/compare-retrieval.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
base='https://fieldlight.megan373lab.xyz'
context=ssl.create_default_context(cafile='/etc/ssl/cert.pem') if sys.platform=='darwin' else ssl.create_default_context()
def call(path,body=None,token=None):
 headers={'User-Agent':'FieldlightResearchCheck/1.0'}
 if body is not None:headers.update({'Content-Type':'application/json','Origin':base,'X-App-Token':token})
 req=Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
 with urlopen(req,context=context,timeout=90) as response:return json.load(response)
config=call('/api/config')
assert config['mode']=='live' and config['expanded'] is True
bundle_path=ROOT/'corpus/photography-expanded.json'
bundle=json.loads(bundle_path.read_text())
chunks=[c for d in bundle['documents'] for c in d['chunks']]
byid={c['source_id']:{**c,'url':d['url']} for d in bundle['documents'] for c in d['chunks']}
rag_spec=importlib.util.spec_from_file_location('rag',ROOT/'scripts/ask-photography.py')
rag=importlib.util.module_from_spec(rag_spec);rag_spec.loader.exec_module(rag)
output={'date_label':'2026-11-14 America/New_York','started_utc':datetime.now(timezone.utc).isoformat(),
 'corpus_sha256':hashlib.sha256(bundle_path.read_bytes()).hexdigest(),'corpus_passages':7,
 'keyword_method':'Unique exact token overlap with explicit stopwords; same stored text; ties by source ID, including zero-score filler; top 4.',
 'vector_method':'Live Qdrant Cloud MiniLM retrieval observed through public app; passage order preserved by backend; top 4. Model-generated answer not included in retrieval metric.',
 'selection_note':'Small purposively chosen set. P2 is an added lexical-mismatch stress case selected before vector execution, not a random held-out sample. No statistical or general accuracy claim.',
 'results':[]}
path=ROOT/'docs/public/retrieval-comparison.json'
path.parent.mkdir(parents=True,exist_ok=True)
for index,(case,question,expected) in enumerate(b.QUESTIONS):
 if index:time.sleep(22)
 try: data=call('/api/ask',{'question':question},config['token'])
 except HTTPError as error:
  output['results'].append({'case':case,'question':question,'not_completed':True,'http_status':error.code})
  path.write_text(json.dumps(output,indent=2,ensure_ascii=False))
  print(case+': HTTP '+str(error.code)+'; not scored',flush=True)
  continue
 ranked=b.baseline(question,chunks)
 vector_ids=[p['source_id'] for p in data.get('passages',[])]
 for passage in data.get('passages',[]):
  expected_passage=rag.separate_pilot_annotations(byid[passage['source_id']])
  assert passage['text']==expected_passage['text'] and passage['url']==expected_passage['url'], 'Hosted corpus differs from local manifest'
 def metrics(ids):
  if not expected:return {'recall_at_4':None,'reciprocal_rank_at_4':None}
  ranks=[i+1 for i,value in enumerate(ids) if value in expected]
  return {'recall_at_4':len(set(ids)&set(expected))/len(expected),'reciprocal_rank_at_4':1/min(ranks) if ranks else 0}
 row={'case':case,'question':question,'expected_evidence_ids':expected,'keyword':{'ranking':ranked,**metrics([r['source_id'] for r in ranked])},
  'vector':{'ranking_ids':vector_ids,**metrics(vector_ids)},'answer_status':data.get('status'),'observed_public_response':data,'returned_text_matches_local_paraphrase_manifest':True}
 output['results'].append(row)
 path.write_text(json.dumps(output,indent=2,ensure_ascii=False))
 print(case+': keyword='+str(row['keyword']['recall_at_4'])+' vector='+str(row['vector']['recall_at_4'])+' ids='+','.join(vector_ids),flush=True)
positives=[r for r in output['results'] if r.get('expected_evidence_ids') and not r.get('not_completed')]
output['summary']={method:{'answerable_questions':len(positives),'macro_recall_at_4':statistics.mean(r[method]['recall_at_4'] for r in positives),'mean_reciprocal_rank_at_4':statistics.mean(r[method]['reciprocal_rank_at_4'] for r in positives)} for method in ('keyword','vector')} if positives else {}
output['finished_utc']=datetime.now(timezone.utc).isoformat()
path.write_text(json.dumps(output,indent=2,ensure_ascii=False))
print('Comparison saved: '+str(path),flush=True)
