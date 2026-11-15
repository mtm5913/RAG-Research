#!/usr/bin/env python3
"""Run five live NPS-pilot questions with one private key entry per provider."""
import getpass
import importlib.util
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
spec = importlib.util.spec_from_file_location('rag', Path(__file__).with_name('ask-photography.py'))
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)
questions = [
 ('E1', 'What starting settings could I try for a starry sky with a tripod, and how should I focus?', ['PHOTO-05-C01','PHOTO-05-C02','PHOTO-05-C03'], 'Checklist preserves tripod/manual mode, conditional starting settings and manual focus. No R1-specific guarantee.'),
 ('E2', 'How can I photograph stars without streaks, and what exposure range does this guide suggest?', ['PHOTO-05-C02'], '10–20 seconds is experimental, not a guaranteed no-trails threshold.'),
 ('E3', 'What exact EOS R1 menu buttons turn on remote shooting?', [], 'Acknowledge absent R1 menu instructions; invent no menu paths.'),
 ('E4', 'Should I use autofocus or focus on a faraway bright object for this setup?', ['PHOTO-05-C03'], 'Manual focus using a distant bright light; no unsupported autofocus mode.'),
 ('E5', 'What shutter speed freezes a basketball player indoors?', [], 'Acknowledge missing sports evidence; do not transfer long night-sky exposures to sports.')
]
print('Runs five live requests to each provider. Sends only the listed photography questions and NPS pilot passages. Keys remain in memory.')
try:
 qkey = rag.clean_key(getpass.getpass('Qdrant API key (hidden): '), 'Qdrant')
 gkey = rag.clean_key(getpass.getpass('Groq API key (hidden): '), 'Groq')
except ValueError as error:
 sys.exit(str(error))
for case, question, expected, review in questions:
 try:
  result = rag.answer(question, qkey, gkey, real=True)
  returned = {p['source_id'] for p in result.get('passages', [])}
  print(json.dumps({'case': case, 'question': question, 'expected_evidence_ids': expected,
   'expected_ids_retrieved': set(expected).issubset(returned) if expected else None,
   'manual_review_required': review, 'result': result}, ensure_ascii=False))
 except HTTPError as error:
  print(json.dumps({'case': case, 'error': 'HTTP '+str(error.code), 'not_executed_to_completion': True}))
  break
 except (URLError, TimeoutError, rag.ResponseError):
  print(json.dumps({'case': case, 'error': 'Connection or response failure; no credentials printed', 'not_executed_to_completion': True}))
  break
