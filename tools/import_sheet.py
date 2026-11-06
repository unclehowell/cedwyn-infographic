#!/usr/bin/env python3
"""One-way import from the old parcel workbook (Google Sheet) into data/*.json. Optional; the repo wins.
The page no longer reads the workbook. Run this only if rows were edited in the sheet and should come into the repo:
  python3 tools/import_sheet.py            # dry run: lists what would change
  python3 tools/import_sheet.py --write    # writes data/*.json, then run tools/build.py
Values are typed by data/schema.graphql (numbers, yes/no -> true/false, empty -> null). Columns the schema does not
know are refused. Nothing is ever written back to the sheet. — Sion's Tab agent"""
import csv, io, json, pathlib, sys, urllib.request
W = pathlib.Path(__file__).resolve().parent; ROOT = W.parent
sys.path.insert(0, str(W)); import gql
SHEET = '1UwUs_CkxZ1dSsNwZWbp2vI9TeR_oLPPJNn5SZhAoRNg'
GIDS = {'maps': 1728723331, 'parcels': 1424590373, 'title_events': 1821955350, 'parties': 2126462563, 'settings': 938231331}
schema = gql.parse_schema((ROOT/'data/schema.graphql').read_text())
def coerce(col, v):
    if v == '': return None
    t = col['type']
    if t == 'Int': return int(float(v))
    if t == 'Float': return float(v)
    if t == 'Boolean': return v.strip().lower() in ('yes', 'true', '1')
    return v
changed = 0
for f, gid in GIDS.items():
    ty = schema['types'][gql.table_type(schema, f)]
    cols = {k: c for k, c in ty['fields'].items() if not c['ref']}
    u = f'https://docs.google.com/spreadsheets/d/{SHEET}/export?format=csv&gid={gid}'
    rows = list(csv.DictReader(io.StringIO(urllib.request.urlopen(u, timeout=30).read().decode('utf-8'))))
    extra = set(rows[0]) - set(cols) if rows else set()
    if extra: sys.exit(f'{f}: the sheet has columns the schema does not know: {sorted(extra)} (add them to data/schema.graphql first)')
    new = [{k: coerce(c, r.get(k, '')) for k, c in cols.items()} for r in rows]
    p = ROOT/'data'/(f + '.json'); doc = json.loads(p.read_text())
    if new != doc['rows']:
        changed += 1
        print(f'{f}: {len(doc["rows"])} rows in the repo, {len(new)} in the sheet, differs')
        if '--write' in sys.argv:
            doc['rows'] = new
            lines = ',\n'.join('    ' + json.dumps(r, ensure_ascii=False) for r in new)
            head = json.dumps({k: v for k, v in doc.items() if k != 'rows'}, ensure_ascii=False, indent=2)[:-2]
            p.write_text(head + ',\n  "rows": [\n' + lines + '\n  ]\n}\n')
    else:
        print(f'{f}: same as the repo')
errs = gql.check(schema, {f: json.loads((ROOT/'data'/(f + '.json')).read_text())['rows'] for f in GIDS})
print('schema check:', 'ok' if not errs else errs[:10])
print(('written; now run python3 tools/build.py' if '--write' in sys.argv else 'dry run') if changed else 'nothing to import')
