#!/usr/bin/env python3
"""Local tokenizer/boundary comparison. Does not change the cloud index."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import tokenizers
from tokenizers import Tokenizer
ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tokenizer',required=True)
parser.add_argument('--headers',help='Optional download headers for the model revision')
args=parser.parse_args()
tokenizer=Tokenizer.from_file(args.tokenizer);tokenizer.no_truncation();tokenizer.no_padding()
spec=importlib.util.spec_from_file_location('rag',ROOT/'scripts/ask-photography.py')
rag=importlib.util.module_from_spec(spec);spec.loader.exec_module(rag)
bundle_path=ROOT/'corpus/photography-expanded.json'
bundle=json.loads(bundle_path.read_text())
documents=[];heading=[];units=[]
for doc in bundle['documents']:
 text='';offsets={}
 for chunk in doc['chunks']:
  if text:text+='\n\n'
  start=len(text);text+=chunk['text'];end=len(text)
  offsets[chunk['source_id']]=(start,end)
  heading.append({'id':chunk['source_id'],'document_id':doc['document_id'],'start':start,'end':end,'text':chunk['text'],'sections':[chunk['section']]})
 for fact_id,(source_id,label,sentence) in rag.CHECKLIST_FACTS.items():
  if source_id not in offsets:continue
  a,b=offsets[source_id];start=text.index(sentence,a,b)
  units.append({'id':fact_id,'document_id':doc['document_id'],'start':start,'end':start+len(sentence),'kind':'complete checked fact wording'})
 # A joined context probe: exposure suggestions through the conditional star-trail sentence.
 if doc['document_id']=='PHOTO-05':
  a,b=offsets['PHOTO-05-C02'];start=text.index('NPS suggests',a,b);finish=text.index('Longer exposures can produce star trails as Earth rotates.',a,b)+len('Longer exposures can produce star trails as Earth rotates.')
  units.append({'id':'exposure_with_qualifier_and_trails','document_id':doc['document_id'],'start':start,'end':finish,'kind':'context span, including the separately labeled project qualifier in stored text'})
 documents.append({'id':doc['document_id'],'text':text,'offsets':offsets,'sections':{c['source_id']:c['section'] for c in doc['chunks']}})

def fixed(size,overlap):
 chunks=[]
 for doc in documents:
  encoding=tokenizer.encode(doc['text'],add_special_tokens=False)
  for index,start in enumerate(range(0,len(encoding.ids),size-overlap)):
   end=min(start+size,len(encoding.ids));char_start=encoding.offsets[start][0];char_end=encoding.offsets[end-1][1]
   sections=[doc['sections'][sid] for sid,(a,b) in doc['offsets'].items() if a<char_end and b>char_start]
   chunks.append({'id':doc['id']+'-W'+str(index+1),'document_id':doc['id'],'start':char_start,'end':char_end,'text':doc['text'][char_start:char_end],'sections':sections})
   if end==len(encoding.ids):break
 return chunks

def analyze(chunks):
 counts=[len(tokenizer.encode(c['text'],add_special_tokens=True).ids) for c in chunks]
 checks=[]
 for unit in units:
  matching=[c for c in chunks if c['document_id']==unit['document_id'] and c['start']<=unit['start'] and c['end']>=unit['end']]
  checks.append({**unit,'complete_in_one_chunk':bool(matching),'containing_chunk_ids':[c['id'] for c in matching]})
 return {'chunks':len(chunks),'min_tokens_with_specials':min(counts),'max_tokens_with_specials':max(counts),'mean_tokens_with_specials':statistics.mean(counts),
  'chunks_over_256_tokens':sum(n>256 for n in counts),'total_stored_tokens_with_specials':sum(counts),
  'crosses_existing_passage_boundaries':sum(len(c['sections'])>1 for c in chunks),'complete_units_in_one_chunk':sum(c['complete_in_one_chunk'] for c in checks),
  'units_checked':len(checks),'unit_checks':checks,'chunk_records':[{**c,'tokens_with_specials':n} for c,n in zip(chunks,counts)]}
revision=None
if args.headers:
 for line in Path(args.headers).read_text().splitlines():
  if line.lower().startswith('x-repo-commit:'):revision=line.split(':',1)[1].strip()
output={'date_label':'2026-11-14 America/New_York','corpus_sha256':hashlib.sha256(bundle_path.read_bytes()).hexdigest(),
 'tokenizer':{'model':'sentence-transformers/all-MiniLM-L6-v2','package_version':tokenizers.__version__,'file_sha256':hashlib.sha256(Path(args.tokenizer).read_bytes()).hexdigest(),'download_revision':revision,'download_url':'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/'+(revision or 'main')+'/tokenizer.json','truncation':'disabled while counting','special_tokens':'included in reported chunk lengths'},
 'scope':'Local representation/boundary check on the same stored paraphrase text, including labeled project annotations; no embedding, indexing or retrieval run for alternative chunkings. Whole fact units are selected to reflect the current extractive app and favor its existing structure; not an independent answer-quality benchmark.',
 'alternatives':{'heading_passages':analyze(heading),'fixed_64_no_overlap':analyze(fixed(64,0)),'fixed_64_overlap_16':analyze(fixed(64,16))}}
path=ROOT/'docs/public/chunking-comparison.json';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(output,indent=2,ensure_ascii=False))
for name,data in output['alternatives'].items():
 print(name, 'chunks',data['chunks'],'max tokens',data['max_tokens_with_specials'],'complete units',str(data['complete_units_in_one_chunk'])+'/'+str(data['units_checked']),'mixed sections',data['crosses_existing_passage_boundaries'])
print('Tokenizer revision:',revision)
