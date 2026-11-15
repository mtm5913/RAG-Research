#!/usr/bin/env python3
"""Reproducible local keyword baseline. No credentials or model calls."""
import json
import re
import unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
STOP=set('a an the and or but to of in on for with as at is are it its this that how what when can i my do does should could try use using me'.split())
QUESTIONS=[
 ('W1','How can I make a waterfall look smoother in a landscape photo?',['PHOTO-06-C02']),
 ('A1','How does aperture affect depth of field in an outdoor landscape photograph?',['PHOTO-06-C03']),
 ('G1','When is golden hour, and what is its light like for landscapes?',['PHOTO-06-C04']),
 ('N1','What starting settings could I try for a starry sky with a tripod, and how should I focus?',['PHOTO-05-C01','PHOTO-05-C02','PHOTO-05-C03']),
 ('P1','How can I give falling water a silky appearance while keeping the camera still?',['PHOTO-06-C02']),
 ('P2','How could I give a cascade a silky appearance rather than freeze its motion?',['PHOTO-06-C02']),
 ('U1','What exact EOS R1 menu buttons turn on remote shooting?',[])
]
def tokens(text):
 return set(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',text).lower()))-STOP

def baseline(question,chunks):
 query=tokens(question)
 result=[]
 for chunk in chunks:
  # Search the same stored text used for embeddings, excluding headings/URLs.
  shared=sorted(query & tokens(chunk['text']))
  result.append({'source_id':chunk['source_id'],'score':len(shared),'matched_terms':shared})
 return sorted(result,key=lambda r:(-r['score'],r['source_id']))[:4]

def main():
 bundle=json.loads((ROOT/'corpus/photography-expanded.json').read_text())
 chunks=[chunk for doc in bundle['documents'] for chunk in doc['chunks']]
 rows=[]
 for case,question,expected in QUESTIONS:
  ranked=baseline(question,chunks)
  returned={row['source_id'] for row in ranked}
  ranks=[i+1 for i,row in enumerate(ranked) if row['source_id'] in expected]
  rows.append({'case':case,'question':question,'expected_evidence_ids':expected,'ranking':ranked,
   'recall_at_4':len(returned&set(expected))/len(expected) if expected else None,
   'reciprocal_rank_at_4':1/min(ranks) if ranks else (0 if expected else None)})
 print(json.dumps({'method':'unique exact query-token overlap; explicit stopword list; ties by source ID; same stored passage text; top 4',
  'corpus':'photography-expanded.json, 7 passages from 2 documents','results':rows},indent=2))
if __name__=='__main__':main()
