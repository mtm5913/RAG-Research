"""Developer preparation only: assemble checked paraphrases; does not import or activate."""
import json
from pathlib import Path
root = Path(__file__).resolve().parent.parent
old = json.loads((root/'corpus/photography-pilot.json').read_text())
new = {
 'document_id':'PHOTO-06', 'title':"Beginner's Photography Guide", 'publisher':'National Park Service',
 'url':'https://home.nps.gov/articles/photographyguide.htm', 'updated':'2017-04-17', 'accessed':'2026-11-14',
 'permission':'NPS-hosted instructional prose with no separate third-party prose attribution observed. Prose-only reuse assessment under NPS ownership policy; not individual written permission. All credited images, captions and logos excluded.',
 'permission_url':'https://www.nps.gov/aboutus/disclaimer.htm#ownership',
 'representation':'AI-prepared source-derived paraphrases checked against article sections; not original quotations. Independent student reading not claimed.',
 'chunks':[
  {'id':4,'source_id':'PHOTO-06-C01','section':'Composition','text':'The NPS beginner guide suggests using the rule of thirds, surrounding objects as a frame, and leading lines to draw attention to the subject in outdoor photographs.'},
  {'id':5,'source_id':'PHOTO-06-C02','section':'Adjust Your Settings — Shutter speed','text':'For a smoother moving-water effect, the guide suggests a slower shutter speed and keeping the camera steady, preferably on a tripod. It gives no universal waterfall exposure time.'},
  {'id':6,'source_id':'PHOTO-06-C03','section':'Adjust Your Settings — Aperture','text':'The guide explains that a larger lens opening has a lower f-number, admits more light and gives shallower depth of field. A higher f-number can make the background clearer. These are general relationships, not guaranteed landscape sharpness or an EOS R1 setting recipe.'},
  {'id':7,'source_id':'PHOTO-06-C04','section':'When to Shoot — Golden Hour','text':'The guide describes shortly after sunrise or before sunset as golden hour, when sunlight has a warmer appearance and softer lighting.'}
 ]
}
(root/'corpus/photography-expanded.json').write_text(json.dumps({'collection':'photography_expanded_v1','documents':[old,new]},indent=2,ensure_ascii=False))
