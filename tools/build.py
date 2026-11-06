#!/usr/bin/env python3
"""Build /infographic/: inline data/transfers.json, the 59 parcels and the parcel database (data/db/*.csv) into the template, run the public-words gate."""
import json, re, pathlib, sys
W = pathlib.Path(__file__).resolve().parent
SITE = W/'site' if (W/'site').exists() else W.parent  # work dir or repo tools/
data = json.load(open(SITE/'public/data/transfers.json'))
parcels = json.load(open(SITE/'public/data/stewart-parcels.json'))
# v3.9.0: the parcel database, one CSV per workbook tab (maps, parcels, title_events, settings); source.json names the linked workbook
import csv
DBDIR = SITE/'public/data/db'
db = {t: list(csv.DictReader(open(DBDIR/(t + '.csv'), newline=''))) for t in ('maps', 'parcels', 'title_events', 'settings')}
db['source'] = json.load(open(DBDIR/'source.json'))
for r in db['parcels']: assert r['map_id'] in {m['map_id'] for m in db['maps']}, r
for r in db['title_events']: assert r['event_id'] and r['interest'], r
(SITE/'public/data/db.json').write_text(json.dumps(db, ensure_ascii=False, indent=0))
BANNED = ['says','claims','according to','hearsay','unverified','alleged','fraud','stolen','branwen','sion','heraldry','heraldic','coat of arms']
def human(d):
    if isinstance(d, dict): return [s for k, v in d.items() if k != 'u' for s in human(v)]
    if isinstance(d, list): return [s for v in d for s in human(v)]
    return [d] if isinstance(d, str) else []
tpl = (W/'template.html').read_text()
visible = re.sub(r'<script>.*?</script>|<style>.*?</style>|<[^>]+>', ' ', tpl, flags=re.S)
text = '\n'.join(human(data)) + '\n' + '\n'.join(human(parcels)) + '\n' + '\n'.join(human(db)) + '\n' + visible
# v2.9: exempt the single outside marker label from the public-words scan
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
html = tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
html = html.replace('/*__DB__*/null', json.dumps(db, ensure_ascii=False).replace('</', '<\\/'))
html = html.replace('/*__PARCELS59__*/null', json.dumps(parcels, ensure_ascii=False).replace('</', '<\\/'))
(SITE/'public/index.html').write_text(html)
print('built', len(data['transfers']), 'transfers', len(data['parties']), 'parties', len(db['parcels']), 'parcel rows', len(db['title_events']), 'title events')
