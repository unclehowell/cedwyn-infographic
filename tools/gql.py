#!/usr/bin/env python3
"""gql.py: a small, dependency-free GraphQL subset for a static repo database (no server).
- parse_schema(sdl): enums, object types with @table(file, key) and @ref(table, from, to) fields, the Query type.
- check(schema, tables): every row of every @table file must match its type exactly (no unknown or missing
  fields, non-null, Int/Float/Boolean/String/ID/enum), keys unique, @ref values resolvable. Returns a list of errors.
- execute(schema, tables, query_text): runs one query (fields, aliases, equality arguments, nested @ref objects;
  no fragments or variables) and returns {"data": ...} exactly as a GraphQL server would for that query.
Used by tools/build.py to compile the persisted queries in data/queries/ into static JSON. — Sion's Tab agent"""
import re, json
TOK = re.compile(r'"""[\s\S]*?"""|"(?:\\.|[^"\\])*"|#[^\n]*|[A-Za-z_][A-Za-z0-9_]*|-?\d+(?:\.\d+)?|[{}()\[\]:!@,=]')
def tokens(s):
    return [t for t in TOK.findall(s) if not t.startswith('#')]
SCALARS = {'Int', 'Float', 'Boolean', 'String', 'ID'}

def parse_schema(sdl):
    t = tokens(sdl); i = 0; enums = {}; types = {}; query = {}
    def args_block():
        nonlocal i
        out = {}
        if i < len(t) and t[i] == '(':
            i += 1
            while t[i] != ')':
                if t[i] == ',': i += 1; continue
                k = t[i]; i += 2  # name :
                if t[i] == '[': i += 1; v = t[i]; i += 1
                    # list arg types are not used here
                else: v = t[i]; i += 1
                while t[i] in ('!', ']'): i += 1
                if t[i] == '=': i += 2
                out[k] = v.strip('"') if v.startswith('"') else v
            i += 1
        return out
    def directives():
        nonlocal i
        d = {}
        while i < len(t) and t[i] == '@':
            name = t[i + 1]; i += 2; d[name] = args_block()
        return d
    while i < len(t):
        w = t[i]
        if w.startswith('"'): i += 1; continue
        if w == 'schema':
            while t[i] != '}': i += 1
            i += 1; continue
        if w == 'enum':
            name = t[i + 1]; i += 3; vals = []
            while t[i] != '}':
                if not t[i].startswith('"'): vals.append(t[i])
                i += 1
            enums[name] = vals; i += 1; continue
        if w == 'type':
            name = t[i + 1]; i += 2; d = directives(); i += 1  # {
            fields = {}
            while t[i] != '}':
                if t[i].startswith('"'): i += 1; continue
                f = t[i]; i += 1; fargs = args_block(); i += 1  # :
                lst = False
                if t[i] == '[': lst = True; i += 1
                base = t[i]; i += 1; nn = False
                if t[i] == '!': nn = True; i += 1
                if lst:
                    i += 1  # ]
                    if i < len(t) and t[i] == '!': i += 1
                fd = directives()
                fields[f] = {'type': base, 'nonnull': nn, 'list': lst, 'args': fargs, 'ref': fd.get('ref')}
            i += 1
            if name == 'Query': query = fields
            else: types[name] = {'fields': fields, 'table': d.get('table')}
            continue
        i += 1
    return {'enums': enums, 'types': types, 'query': query}

def table_type(schema, file):
    for n, ty in schema['types'].items():
        if ty['table'] and ty['table']['file'] == file: return n
    raise KeyError(file)

def check(schema, tables):
    errs = []
    for n, ty in schema['types'].items():
        if not ty['table']: continue
        f = ty['table']['file']; rows = tables.get(f)
        if rows is None: errs.append(f'{f}.json missing'); continue
        cols = {k: v for k, v in ty['fields'].items() if not v['ref']}
        keys = ty['table']['key'].split(',')
        seen = set()
        for j, r in enumerate(rows):
            where = f'{f}.json row {j + 1}'
            if not isinstance(r, dict): errs.append(f'{where}: not an object'); continue
            for k in r:
                if k not in cols: errs.append(f'{where}: unknown field "{k}"')
            for k, c in cols.items():
                if k not in r: errs.append(f'{where}: missing field "{k}" (use null when empty)'); continue
                v = r[k]; ty_ = c['type']
                if v is None:
                    if c['nonnull']: errs.append(f'{where}: "{k}" may not be null')
                    continue
                ok = (ty_ == 'Int' and isinstance(v, int) and not isinstance(v, bool)) or \
                     (ty_ == 'Float' and isinstance(v, (int, float)) and not isinstance(v, bool)) or \
                     (ty_ == 'Boolean' and isinstance(v, bool)) or \
                     (ty_ in ('String', 'ID') and isinstance(v, str)) or \
                     (ty_ in schema['enums'] and v in schema['enums'][ty_])
                if not ok:
                    hint = f' (one of {", ".join(schema["enums"][ty_])})' if ty_ in schema['enums'] else ''
                    errs.append(f'{where}: "{k}" should be {ty_}{hint}, got {json.dumps(v, ensure_ascii=False)[:60]}')
                elif c['nonnull'] and ty_ in ('String', 'ID') and v == '':
                    errs.append(f'{where}: "{k}" may not be empty')
            kv = tuple(r.get(k) for k in keys)
            if kv in seen: errs.append(f'{where}: duplicate key {kv}')
            seen.add(kv)
        for k, c in ty['fields'].items():
            ref = c['ref']
            if not ref: continue
            target = {x.get(ref['to']) for x in tables.get(ref['table'], [])}
            for j, r in enumerate(rows):
                v = r.get(ref['from'])
                if v not in (None, '') and v not in target:
                    errs.append(f'{f}.json row {j + 1}: "{ref["from"]}" = {v!r} is not a {ref["table"]} {ref["to"]}')
    return errs

def _parse_sel(t, i):
    """selection set starting at t[i] == '{' -> (list of (alias, name, args, subsel)), next index"""
    assert t[i] == '{', t[i]; i += 1; out = []
    while t[i] != '}':
        if t[i] == ',': i += 1; continue
        name = t[i]; i += 1; alias = name
        if t[i] == ':': alias = name; name = t[i + 1]; i += 2
        args = {}
        if t[i] == '(':
            i += 1
            while t[i] != ')':
                if t[i] == ',': i += 1; continue
                k = t[i]; v = t[i + 2]; i += 3
                if v.startswith('"'): v = json.loads(v)
                elif re.fullmatch(r'-?\d+', v): v = int(v)
                elif re.fullmatch(r'-?\d+\.\d+', v): v = float(v)
                elif v in ('true', 'false'): v = v == 'true'
                elif v == 'null': v = None
                args[k] = v
            i += 1
        sub = None
        if i < len(t) and t[i] == '{': sub, i = _parse_sel(t, i)
        out.append((alias, name, args, sub))
    return out, i + 1

def _resolve(schema, tables, tyname, row, sel):
    ty = schema['types'][tyname]; o = {}
    for alias, name, args, sub in sel:
        if name not in ty['fields']: raise ValueError(f'{tyname} has no field {name}')
        c = ty['fields'][name]
        if c['ref']:
            ref = c['ref']; v = row.get(ref['from'])
            hit = next((x for x in tables[ref['table']] if v not in (None, '') and x.get(ref['to']) == v), None)
            o[alias] = _resolve(schema, tables, c['type'], hit, sub) if hit is not None else None
        else:
            if sub: raise ValueError(f'{tyname}.{name} is a scalar')
            o[alias] = row.get(name)
    return o

def execute(schema, tables, text):
    t = tokens(text); i = 0
    while t[i] != '{': i += 1
    sel, _ = _parse_sel(t, i); data = {}
    for alias, name, args, sub in sel:
        if name not in schema['query']: raise ValueError(f'Query has no field {name}')
        q = schema['query'][name]; tyname = q['type']; f = schema['types'][tyname]['table']['file']
        for a in args:
            if a not in q['args']: raise ValueError(f'{name} takes no argument {a}')
        rows = [r for r in tables[f] if all(r.get(a) == v for a, v in args.items())]
        if not sub: raise ValueError(f'{name} needs a selection')
        data[alias] = [_resolve(schema, tables, tyname, r, sub) for r in rows]
    return {'data': data}
