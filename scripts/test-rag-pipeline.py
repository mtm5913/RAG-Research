import importlib.util
import json
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('rag', Path(__file__).with_name('ask-photography.py'))
rag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag)
corpus = json.loads((Path(__file__).resolve().parent.parent/'corpus/photography-pilot.json').read_text())

class PipelineChecks(unittest.TestCase):
    def run_real(self, selection, transform=None, finish='stop'):
        calls = []
        points = [{'payload': {**chunk, 'synthetic': False, 'url': corpus['url']}} for chunk in corpus['chunks']]
        if transform: points = transform(points)
        def request(url, body, headers):
            calls.append(body)
            if 'points/query' in url:
                return {'result': {'points': points}}
            content = selection if isinstance(selection, str) else json.dumps(selection)
            return {'choices': [{'finish_reason': finish, 'message': {'content': content}}]}
        result = rag.answer('night sky?', 'dummy', 'dummy', request=request, real=True)
        return result, calls
    def test_selected_words_are_owned_by_server(self):
        result, _ = self.run_real({'answerable': True, 'fact_ids': ['settings','focus']})
        self.assertEqual(result['status'], 'generated')
        self.assertEqual(result['answer_method'], 'source_checklist_v1')
        self.assertNotIn('live view', result['answer'])
        for fact_id in result['selected_fact_ids']:
            source_id, label, text = rag.CHECKLIST_FACTS[fact_id]
            self.assertIn(text+' ['+source_id+']', result['answer'])
    def test_exposure_includes_context_and_conditional_warning(self):
        result, _ = self.run_real({'answerable': True, 'fact_ids': ['settings']})
        self.assertIn('equipment', result['selected_fact_ids'])
        self.assertIn('trails', result['selected_fact_ids'])
        self.assertIn('does not guarantee', result['answer'])
    def test_false_is_deterministic_refusal(self):
        result, _ = self.run_real({'answerable': False, 'fact_ids': []})
        self.assertEqual(result['status'], 'insufficient_evidence')
        self.assertNotIn('10 to 20', result['answer'])
    def test_added_answer_text_rejected(self):
        result, _ = self.run_real({'answerable': True, 'fact_ids': ['focus'], 'answer':'Use live view and ISO 12800'})
        self.assertEqual(result['status'],'answer_withheld')
        self.assertNotIn('12800',result['answer'])
    def test_unknown_fact_rejected(self):
        result,_=self.run_real({'answerable':True,'fact_ids':['sports_shutter']})
        self.assertEqual(result['status'],'answer_withheld')
    def test_duplicate_facts_rejected(self):
        result,_=self.run_real({'answerable':True,'fact_ids':['focus','focus']})
        self.assertEqual(result['status'],'answer_withheld')
    def test_invalid_json_rejected(self):
        result,_=self.run_real('Here is some advice: zoom in.')
        self.assertEqual(result['status'],'answer_withheld')
    def test_truncated_selection_rejected(self):
        result,_=self.run_real({'answerable':True,'fact_ids':['focus']},finish='length')
        self.assertEqual(result['status'],'answer_withheld')
    def test_annotation_not_in_generator_input(self):
        result,calls=self.run_real({'answerable':True,'fact_ids':['focus']})
        data=json.loads(calls[1]['messages'][1]['content'])
        self.assertNotIn('project_annotations',json.dumps(data))
        self.assertNotIn('menu paths',json.dumps(data))
        format = calls[1]['response_format']
        self.assertEqual(format['type'], 'json_schema')
        self.assertTrue(format['json_schema']['strict'])
        self.assertIn('focus', format['json_schema']['schema']['properties']['fact_ids']['items']['enum'])
        self.assertTrue(result['passages'][0]['project_annotations'])
    def test_unrecognized_source_wording_skips_generation(self):
        def transform(points):
            for point in points:point['payload']['text']='Tampered text with arbitrary settings.'
            return points
        result,calls=self.run_real({'answerable':True,'fact_ids':['settings']},transform)
        self.assertEqual(result['status'],'insufficient_evidence');self.assertEqual(len(calls),1)
    def test_wrong_source_url_skips_generation(self):
        def transform(points):
            for point in points:point['payload']['url']='https://elsewhere.example'
            return points
        result,calls=self.run_real({'answerable':True,'fact_ids':['focus']},transform)
        self.assertEqual(result['status'],'insufficient_evidence');self.assertEqual(len(calls),1)
    def test_missing_context_cannot_render_settings(self):
        result,_=self.run_real({'answerable':True,'fact_ids':['settings']},lambda points:[points[1]])
        self.assertEqual(result['status'],'answer_withheld')
    def test_inconsistent_refusal_rejected(self):
        result,_=self.run_real({'answerable':False,'fact_ids':['settings']})
        self.assertEqual(result['status'],'answer_withheld')
    def test_boolean_type_checked(self):
        result,_=self.run_real({'answerable':'true','fact_ids':['focus']})
        self.assertEqual(result['status'],'answer_withheld')
    def test_empty_supported_selection_rejected(self):
        result,_=self.run_real({'answerable':True,'fact_ids':[]})
        self.assertEqual(result['status'],'answer_withheld')
    def test_synthetic_path_still_checks_citations(self):
        def request(url,body,headers):
            if 'points/query' in url:return {'result':{'points':[{'payload':{'synthetic':True,'source_id':'SYNTHETIC-01','text':'stars'}}]}}
            return {'choices':[{'finish_reason':'stop','message':{'content':'Invented [SYNTHETIC-99]'}}]}
        self.assertEqual(rag.answer('stars?','dummy','dummy',request=request)['status'],'answer_withheld')
    def test_empty_retrieval_skips_generation(self):
        calls=[]
        def request(*args):calls.append(args);return {'result':{'points':[]}}
        self.assertEqual(rag.answer('question','dummy','dummy',request=request,real=True)['status'],'insufficient_evidence')
        self.assertEqual(len(calls),1)
    def test_key_whitespace_trimmed(self):
        self.assertEqual(rag.clean_key(' example-key\n','Test'),'example-key')
        with self.assertRaises(ValueError):rag.clean_key('example key','Test')

class ExpandedSourceChecks(unittest.TestCase):
    def test_landscape_facts_use_new_source_and_own_wording(self):
        bundle=json.loads((Path(__file__).resolve().parent.parent/'corpus/photography-expanded.json').read_text())
        new=bundle['documents'][1]
        points=[{'payload':{**chunk,'synthetic':False,'url':new['url']}} for chunk in new['chunks']]
        def request(url,body,headers):
            if 'points/query' in url:return {'result':{'points':points}}
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'answerable':True,'fact_ids':['waterfall','aperture','golden_hour']})}}]}
        result=rag.answer('Landscape?', 'dummy','dummy',request=request,real=True)
        self.assertEqual(result['status'],'generated')
        self.assertIn('[PHOTO-06-C02]',result['answer'])
        self.assertNotIn('10 to 20',result['answer'])
        self.assertEqual(result['selected_fact_ids'], ['waterfall'])
        self.assertNotIn('no universal waterfall',result['answer'])
        self.assertNotIn('not guaranteed landscape',result['answer'])
    def test_manifest_ids_unique_and_whitelist_matches(self):
        bundle=json.loads((Path(__file__).resolve().parent.parent/'corpus/photography-expanded.json').read_text())
        chunks=[chunk for doc in bundle['documents'] for chunk in doc['chunks']]
        self.assertEqual(len(chunks),7)
        self.assertEqual(len({c['id'] for c in chunks}),7)
        for _,(source_id,_,sentence) in rag.CHECKLIST_FACTS.items():
            self.assertTrue(any(c['source_id']==source_id and sentence in c['text'] for c in chunks))

    def test_waterfall_excludes_overselected_night_sky_settings(self):
        bundle=json.loads((Path(__file__).resolve().parent.parent/'corpus/photography-expanded.json').read_text())
        points=[{'payload':{**chunk,'synthetic':False,'url':doc['url']}} for doc in bundle['documents'] for chunk in doc['chunks']]
        def request(url,body,headers):
            if 'points/query' in url:return {'result':{'points':points}}
            return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'answerable':True,'fact_ids':['equipment','settings','mode','waterfall']})}}]}
        result=rag.answer('Waterfall blur?','dummy','dummy',request=request,real=True)
        self.assertEqual(result['selected_fact_ids'], ['waterfall'])
        self.assertNotIn('ISO 400',result['answer'])
        self.assertNotIn('PHOTO-05',result['answer'])

unittest.main()
