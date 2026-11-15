#!/usr/bin/env python3
"""Read-only Qdrant connection check; optional SSH execution, no remote writes."""
import argparse
import getpass
import json
import os
import shlex
import subprocess
import sys
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

DEFAULT_URL = 'https://b1ab0886-4597-47ce-9505-021378d92cf8.us-east-2-0.aws.cloud.qdrant.io:6333'
REMOTE_CODE = '''import json,sys
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
cfg=json.load(sys.stdin)
try:
 r=urlopen(Request(cfg['url']+'/collections',headers={'api-key':cfg['key']}),timeout=15)
 data=json.load(r)
 print(json.dumps({'http_status':r.status,'status':data.get('status'),'collections':[c['name'] for c in data.get('result',{}).get('collections',[])]}))
except HTTPError as e:
 print(json.dumps({'http_status':e.code,'status':'authentication or request rejected'}));sys.exit(1)
except (URLError,TimeoutError):
 print(json.dumps({'status':'connection failed; no credentials printed'}));sys.exit(1)
'''

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--url',default=os.environ.get('QDRANT_URL',DEFAULT_URL))
 parser.add_argument('--server',help='SSH user@host; use a host with an already trusted key')
 parser.add_argument('--identity',help='Existing SSH private-key path; never a key value')
 args=parser.parse_args()
 parsed=urlparse(args.url)
 if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('','/'):
  parser.error('Use a plain HTTPS Qdrant endpoint without credentials, query or path.')
 url=args.url.rstrip('/')
 if not args.server:
  print('Target: Qdrant API from this computer.')
 else:
  if args.server.startswith('-') or any(c.isspace() for c in args.server):parser.error('Invalid SSH target.')
  print('Target: read-only Qdrant API check from '+args.server+'. No server files will be written.')
 key=os.environ.get('QDRANT_API_KEY') or getpass.getpass('Qdrant API key (hidden; sent only to the chosen server/Qdrant): ')
 if not key.strip():parser.error('An API key is required.')
 if args.server:
  cmd=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10']
  if args.identity:cmd+=['-i',os.path.expanduser(args.identity),'-o','IdentitiesOnly=yes']
  cmd+=[args.server,'python3 -c '+shlex.quote(REMOTE_CODE)]
  try:
   result=subprocess.run(cmd,input=json.dumps({'url':url,'key':key}),text=True,timeout=30)
   return result.returncode
  except subprocess.TimeoutExpired:
   print('SSH/API check timed out. No key printed.',file=sys.stderr);return 1
 try:
  with urlopen(Request(url+'/collections',headers={'api-key':key}),timeout=15) as response:
   data=json.load(response)
   print(json.dumps({'http_status':response.status,'status':data.get('status'),'collections':[c['name'] for c in data.get('result',{}).get('collections',[])]}))
   return 0
 except HTTPError as error:
  print('Request rejected: HTTP '+str(error.code)+'. No key printed.',file=sys.stderr);return 1
 except (URLError,TimeoutError):
  print('Connection failed. No key printed.',file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
