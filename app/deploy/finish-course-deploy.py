#!/usr/bin/env python3
"""Finish the staged course-server deployment using private prompts."""
import argparse
import getpass
import json
import shlex
import subprocess
import sys

SSH=['ssh','-i','/Users/meganmcneal/.ssh/is373_digitalocean','-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10','deploy@137.184.201.122']
DNS_CHECK='''import json,subprocess
r=subprocess.run(['dig','+short','+time=3','+tries=1','A','fieldlight.megan373lab.xyz'],capture_output=True,text=True,timeout=8)
print(json.dumps({'dns_ready':'137.184.201.122' in r.stdout.splitlines()}))
'''
FINISH='''import json,os,subprocess,time
from pathlib import Path
from urllib.request import Request,urlopen
cfg=json.load(__import__('sys').stdin)
root=Path('/home/deploy/fieldlight')
release=Path((root/'staged-release').read_text().strip()).resolve()
assert release.parent == root/'releases'
# Validate existing provider access before persisting either credential.
checks=[('https://b1ab0886-4597-47ce-9505-021378d92cf8.us-east-2-0.aws.cloud.qdrant.io:6333/collections/photography_expanded_v1',{'api-key':cfg['qdrant']}),('https://api.groq.com/openai/v1/models',{'Authorization':'Bearer '+cfg['groq']})]
for url,headers in checks:
 with urlopen(Request(url,headers={'User-Agent':'PhotographyResearchApp/0.1',**headers}),timeout=15) as response:
  assert response.status==200
secret_dir=root/'secrets';secret_dir.mkdir(mode=0o700,exist_ok=True);os.chmod(secret_dir,0o700)
for name,value in [('qdrant_key',cfg['qdrant']),('groq_key',cfg['groq'])]:
 path=secret_dir/name
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
 with os.fdopen(fd,'w') as file:file.write(value)
 os.chmod(path,0o600)
def compose(*args):
 return subprocess.run(['docker','compose','--env-file','deployment.env',*args],cwd=release,check=True,capture_output=True,text=True)
def wait_healthy():
 cid=compose('ps','-q','app').stdout.strip()
 for _ in range(20):
  status=subprocess.run(['docker','inspect','--format','{{.State.Health.Status}}',cid],capture_output=True,text=True,check=True).stdout.strip()
  if status=='healthy':return
  time.sleep(2)
 raise RuntimeError('Container health check did not pass')
compose('up','-d');wait_healthy()
(release/'deployment.env').write_text('APP_UID=1000\\nAPP_GID=1000\\nAPP_ROUTE_ENABLED=true\\n')
compose('up','-d');wait_healthy()
print(json.dumps({'status':'healthy','url':'https://fieldlight.megan373lab.xyz','certificate_verification':'pending external check','keys_saved':'course server only; file mode 600','existing_services':'not restarted'}))
'''

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--check-only',action='store_true',help='Check DNS only; no key prompts or server writes')
 args=parser.parse_args()
 try:
  probe=subprocess.run(SSH+['python3 -c '+shlex.quote(DNS_CHECK)],capture_output=True,text=True,check=True,timeout=20)
  ready=json.loads(probe.stdout)['dns_ready']
 except (subprocess.SubprocessError,ValueError,KeyError):
  sys.exit('Could not verify server/DNS readiness. No key entered or printed.')
 if not ready:
  sys.exit('DNS is not ready. In Porkbun, add A record fieldlight → 137.184.201.122 for megan373lab.xyz. No keys entered or saved.')
 if args.check_only:
  print('DNS ready. No server changes made.');return
 print('This stores your existing Qdrant and Groq keys only on your course server in /home/deploy/fieldlight/secrets (private files, mode 600).')
 print('It starts only Fieldlight and enables its HTTPS route after container health checks. Keys never enter GitHub or the browser.')
 qkey=getpass.getpass('Qdrant API key (hidden): ').strip()
 gkey=getpass.getpass('Groq API key (hidden): ').strip()
 for key in (qkey,gkey):
  if not key or not key.isascii() or any(c.isspace() for c in key):sys.exit('Invalid key format. No key saved or printed.')
 try:
  result=subprocess.run(SSH+['python3 -c '+shlex.quote(FINISH)],input=json.dumps({'qdrant':qkey,'groq':gkey}),capture_output=True,text=True,timeout=110)
  if result.returncode:
   sys.exit('Deployment did not complete. No key printed. Ask for a read-only deployment check; do not paste credentials or server logs containing them.')
  print(result.stdout.strip())
 except subprocess.TimeoutExpired:
  sys.exit('Deployment check timed out; the server may still be starting. No key printed. Ask for a read-only status check.')

if __name__=='__main__':main()
