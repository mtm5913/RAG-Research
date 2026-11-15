import importlib.util
import json
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
spec = importlib.util.spec_from_file_location('appserver', Path(__file__).with_name('server.py'))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class BrowserAPI(unittest.TestCase):
    def setUp(self):
        self.calls = []
        def query(question):
            self.calls.append(question)
            return {'status':'generated','answer':'Manual mode [PHOTO-05-C01]',
                    'unvalidated_draft_for_review':'DO NOT EXPOSE', 'usage':{'secret':'DO NOT EXPOSE'},
                    'passages':[{'source_id':'PHOTO-05-C01','text':'Use manual mode.','url':'https://home.nps.gov/','section':'Equipment', 'project_annotations':['DO NOT EXPOSE']}]}
        self.server = app.AppServer(('127.0.0.1',0),query)
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True); self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()
    def post(self,body,**extra):
        headers={'Content-Type':'application/json','Origin':self.url,'X-App-Token':self.server.csrf,**extra}
        return urlopen(Request(self.url+'/api/ask',data=json.dumps(body).encode(),headers=headers),timeout=5)
    def test_real_route_and_private_fields(self):
        with self.post({'question':'Focus?'}) as response:
            raw=response.read().decode(); data=json.loads(raw)
            self.assertEqual(data['mode'],'live'); self.assertNotIn('DO NOT EXPOSE',raw)
            self.assertEqual(self.calls,['Focus?'])
    def test_cross_origin_rejected_before_provider(self):
        with self.assertRaises(HTTPError) as error:
            self.post({'question':'Focus?'},Origin='https://elsewhere.example')
        self.assertEqual(error.exception.code,403); self.assertEqual(self.calls,[])
    def test_question_limit_before_provider(self):
        with self.assertRaises(HTTPError) as error:self.post({'question':'x'*1001})
        self.assertEqual(error.exception.code,400); self.assertEqual(self.calls,[])
    def test_rate_limit(self):
        for _ in range(3):self.post({'question':'Focus?'}).close()
        with self.assertRaises(HTTPError) as error:self.post({'question':'Focus?'})
        self.assertEqual(error.exception.code,429); self.assertEqual(len(self.calls),3)
    def test_saved_example_labels(self):
        request=Request(self.url+'/api/example',data=b'{"case":"E1"}',headers={'Content-Type':'application/json','Origin':self.url,'X-App-Token':self.server.csrf})
        with urlopen(request) as response:data=json.load(response)
        self.assertEqual(data['mode'],'saved_example');self.assertEqual(self.calls,[])
    def test_preview_does_not_call_provider(self):
        self.server.query=None
        with self.assertRaises(HTTPError) as error:self.post({'question':'Focus?'})
        self.assertEqual(error.exception.code,503);self.assertEqual(self.calls,[])
    def test_static_security_headers(self):
        with urlopen(self.url) as response:
            self.assertIn('Fieldlight',response.read().decode())
            self.assertIn("script-src 'self'",response.headers['Content-Security-Policy'])
            self.assertEqual(response.headers['X-Content-Type-Options'],'nosniff')
    def test_path_traversal_not_served(self):
        with self.assertRaises(HTTPError) as error:urlopen(self.url+'/../scripts/check-qdrant.py')
        self.assertEqual(error.exception.code,404)

    def test_public_proxy_requires_expected_https_origin(self):
        self.server.public_host='fieldlight.megan373lab.xyz'
        with self.post({'question':'Focus?'},Host='fieldlight.megan373lab.xyz',Origin='https://fieldlight.megan373lab.xyz') as response:
            self.assertEqual(response.status,200)
        with self.assertRaises(HTTPError) as error:
            self.post({'question':'Focus?'},Host='fieldlight.megan373lab.xyz',Origin='http://fieldlight.megan373lab.xyz')
        self.assertEqual(error.exception.code,403)
    def test_healthcheck_does_not_disclose_credentials(self):
        self.server.public_host='fieldlight.megan373lab.xyz'
        with urlopen(self.url+'/healthz') as response:
            data=json.load(response)
        self.assertEqual(data,{'status':'ok','mode':'live'})

unittest.main()
