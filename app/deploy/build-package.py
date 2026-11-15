#!/usr/bin/env python3
"""Build an allowlisted, credential-free deployment bundle."""
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
stage=Path(tempfile.mkdtemp(prefix='fieldlight-deploy-'))
files=['app/server.py','app/web/index.html','app/web/style.css','app/web/app.js','app/deploy/Dockerfile','scripts/ask-photography.py','docs/public/photography-evaluation-round-3.json']
for name in files:
 target=stage/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
shutil.copyfile(ROOT/'app/deploy/compose.yaml',stage/'compose.yaml')
shutil.copyfile(ROOT/'app/deploy/.dockerignore',stage/'.dockerignore')
(stage/'.local-corpus.json').write_text(json.dumps({'collection':'photography_expanded_v1','documents':2,'passages':7}))
archive=stage.with_suffix('.tar.gz')
with tarfile.open(archive,'w:gz') as tar:
 for file in sorted(stage.rglob('*')):
  if file.is_file():tar.add(file,arcname=str(file.relative_to(stage)))
print(json.dumps({'archive':str(archive),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':[str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()]},indent=2))
