#!/usr/bin/env python3
"""Build /infographic/ (v3.10.0).
Source of truth: data/*.json (typed by data/schema.graphql), public/data/transfers.json (the ring) and
public/data/stewart-parcels.json (the 59 parcel records).
1. check every data/*.json row against data/schema.graphql (types, required fields, unique keys, references);
2. run the persisted queries in data/queries/*.graphql and write each answer to public/api/<name>.json;
3. inline the ring data, the 59 parcels and the page's own query (db) into tools/template.html -> public/index.html;
4. write public/sw.js (the page cache) from tools/sw.js with this build's id;
5. run the public-words gate. Exits non-zero with a plain list of problems if anything is wrong.
No network, no installs: python3 tools/build.py   (--check only validates)."""
import json, re, pathlib, sys, hashlib
W = pathlib.Path(__file__).resolve().parent
ROOT = W.parent
sys.path.insert(0, str(W))
import gql
VERSION = (ROOT/'.version').read_text().strip() if (ROOT/'.version').exists() else '0.0.0'
data = json.load(open(ROOT/'public/data/transfers.json'))
parcels = json.load(open(ROOT/'public/data/stewart-parcels.json'))

# 1. the parcel database: data/<table>.json -> rows, checked against the schema
schema_text = (ROOT/'data/schema.graphql').read_text()
schema = gql.parse_schema(schema_text)
tables, errs = {}, []
for n, ty in schema['types'].items():
    if not ty['table']: continue
    f = ty['table']['file']; p = ROOT/'data'/(f + '.json')
    try:
        doc = json.loads(p.read_text())
        tables[f] = doc['rows'] if isinstance(doc, dict) else doc
    except Exception as e:
        errs.append(f'data/{f}.json: not valid JSON ({e})')
errs += gql.check(schema, tables) if not errs else []
# rules the types cannot say
st = {s['key']: s['value'] for s in tables.get('settings', [])}
for k in ('chain_for_A', 'chain_for_B'):
    if not isinstance(st.get(k), int): errs.append(f'data/settings.json: {k} needs a whole-number value (a parcel number 1-59)')
for r in tables.get('parcels', []):
    if not 1 <= r['parcel_no'] <= 59: errs.append(f'data/parcels.json: parcel_no {r["parcel_no"]} is outside 1-59')
    if (r['family_label'] is None) != (r['family_note'] is None):
        errs.append(f'data/parcels.json: {r["map_id"]} {r["parcel_no"]}: family_label and family_note go together (the family position)')
if errs:
    sys.exit('data problems:\n  ' + '\n  '.join(errs[:60]))

# 2. persisted queries -> public/api/<name>.json
canon = json.dumps([tables, schema_text], sort_keys=True, ensure_ascii=False)
queries = sorted((ROOT/'data/queries').glob('*.graphql'))
qtext = {q.stem: q.read_text() for q in queries}
BUILD = VERSION + '+' + hashlib.sha256((canon + json.dumps(qtext, sort_keys=True) + (W/'template.html').read_text()
        + (W/'sw.js').read_text() + json.dumps([data, parcels], sort_keys=True)).encode()).hexdigest()[:10]
API = ROOT/'public/api'; API.mkdir(parents=True, exist_ok=True)
answers = {}
for name, text in qtext.items():
    try: res = gql.execute(schema, tables, text)
    except Exception as e: sys.exit(f'data/queries/{name}.graphql: {e}')
    res['extensions'] = {'build': BUILD, 'query': name, 'source': 'data/*.json (repo)', 'schema': 'data/schema.graphql'}
    answers[name] = res
    (API/(name + '.json')).write_text(json.dumps(res, ensure_ascii=False, separators=(',', ':')) + '\n')
for old in API.glob('*.json'):
    if old.stem not in qtext: old.unlink()
db = dict(answers['db']['data']); db['v'] = BUILD

# 5. public-words gate (all public text: the ring, the parcels, every query answer and the page's visible words)
BANNED = ['says','claims','according to','hearsay','unverified','alleged','fraud','stolen','branwen','sion','heraldry','heraldic','coat of arms']
def human(d):
    if isinstance(d, dict): return [s for k, v in d.items() if k != 'u' for s in human(v)]
    if isinstance(d, list): return [s for v in d for s in human(v)]
    return [d] if isinstance(d, str) else []
tpl = (W/'template.html').read_text()
visible = re.sub(r'<script>.*?</script>|<style>.*?</style>|<[^>]+>', ' ', tpl, flags=re.S)
text = '\n'.join(human(data) + human(parcels) + human([a['data'] for a in answers.values()])) + '\n' + visible
OWNER_LABEL = 'Permissive occupancy origin (synthetic Parcel A labels; not a title-holder)'
assert [p for p in data['parties'] if p.get('name') == OWNER_LABEL], 'outside synthetic-origin marker missing'
text = text.replace(OWNER_LABEL, ' ')
bad = [w for w in BANNED if re.search(r'\b' + w + r'\b', text, re.I)]
if bad: sys.exit('banned words: %s' % bad)
ids = {p['id'] for p in data['parties']}; pids = {p['id'] for p in data['parcels']}
for t in data['transfers']:
    assert t['from'] in ids and t['to'] in ids, t['id']
    assert all(p in pids for p in t['parcels']), t['id']
    assert t['status'] in ('solid', 'dashed') and (t['status'] == 'solid' or t['reason']), t['id']
    assert str(t['year']) in t['label'], t['id']
    assert t['sources'], t['id']
if '--check' in sys.argv:
    print('ok', BUILD); sys.exit(0)

# 3-4. the page and its cache
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = tpl.replace('/*__DATA__*/null', js(data)).replace('/*__DB__*/null', js(db)).replace('/*__PARCELS59__*/null', js(parcels))
html = html.replace('__BUILD__', BUILD)
(ROOT/'public/index.html').write_text(html)
(ROOT/'public/sw.js').write_text((W/'sw.js').read_text().replace('__BUILD__', BUILD))
print('built', BUILD, '·', len(data['transfers']), 'transfers ·', len(tables['parcels']), 'parcel rows ·',
      len(tables['title_events']), 'title events ·', len(answers), 'queries ->', ', '.join('api/%s.json' % k for k in answers),
      '· index.html %d KB' % (len(html.encode()) // 1024))
