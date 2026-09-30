import json, os, re, html
from html.parser import HTMLParser
from meta import CLASSES, DESC_KEY, BONUS_PREFIX, LANGS, SEASON, UPCOMING, DATA_VERSION
I18N = {l: json.load(open(f'i18n/{l}.json', encoding='utf-8')) for l in LANGS}
cls_src = json.load(open('cls_src.json')); mst_src = json.load(open('mst_src.json')); ab = json.load(open('ab_src.json'))
def icu(s): return s.replace("''", "'") if s else s
def tr(key, l):
    v = I18N[l].get(key) or I18N['en'].get(key)
    return icu(v)

OUT = '..'   # the project root; run from tools/
os.makedirs(f'{OUT}/data/skills', exist_ok=True)

meta = {'classes': [], 'masteries': []}
names = {l: {} for l in LANGS}      # class/mastery key -> name
descs = {l: {} for l in LANGS}
bonus = {l: {} for l in LANGS}
sknames = {l: {} for l in LANGS}
for cid, ckey, cname, ms in CLASSES:
    base = [[i, s['reqCharLevel'], 'L'] for i, s in cls_src.items() if s['classId'] == cid]
    tree = [[i, s['reqLevel'], 'T'] for i, s in mst_src.items() if s['classId'] == cid and s['mastery'] == 0]
    meta['classes'].append({'key': ckey, 'id': cid, 'base': base, 'tree': tree, 'm': [m[0] for m in ms]})
    for l in LANGS:
        names[l][ckey] = tr(f'Common.Class_{cname}', l)
        descs[l][ckey] = tr(f'UI.Class_{cname}_Description', l)
    for mi, (mkey, mname, bkey) in enumerate(ms, start=1):
        sk = [[i, s['reqLevel'], 'M' if s['reqMastery'] else 'T'] for i, s in mst_src.items() if s['classId'] == cid and s['mastery'] == mi]
        sk.sort(key=lambda x: (x[2] != 'M', x[1]))          # the mastery skill first, then by tree points
        meta['masteries'].append({'key': mkey, 'cls': ckey, 'idx': mi, 'skills': sk})
        for l in LANGS:
            names[l][mkey] = tr(f'Common.Mastery_{mname}', l)
            descs[l][mkey] = tr(DESC_KEY.get(mkey, f'UI.Mastery_{mname}_Description'), l)
            pre = BONUS_PREFIX.get(mkey, f'UI.PassiveTree_Panel_{bkey}Bonus')
            bs = []
            for n in range(1, 5):
                v = tr(f'{pre}{n}_Label', l)
                if v: bs.append(v)
            bonus[l][mkey] = bs
for i, a in ab.items():
    for l in LANGS:
        # some abilities come without a nameKey (Arcane Ascendance since version150); the root node
        # of the skill's own tree carries the same name
        sknames[l][i] = (tr(a['nameKey'], l) if a['nameKey'] else None) or tr(f'Skills.Skill_{i}_0_Name', l)
missing = [(l, k) for l in LANGS for k, v in list(names[l].items()) + list(sknames[l].items()) if not v]
print('missing names:', missing[:20])
meta['names'] = names; meta['desc'] = descs; meta['bonus'] = bonus; meta['sk'] = sknames
meta['mana'] = {i: a['mana'] for i, a in ab.items()}
known = {m['key'] for m in meta['masteries']}
meta['season'] = SEASON
have = {v.lower() for v in sknames['en'].values() if v}      # a stub goes by itself once the real skill is in the data
meta['upcoming'] = [{'id': i, 'm': m, 'n': n} for i, m, n in UPCOMING if m in known and n.lower() not in have]
with open(f'{OUT}/data/le.js', 'w', encoding='utf-8') as f:
    f.write('/* Last Epoch classes, masteries and skills — generated from lastepochtools.com data (' + DATA_VERSION + '). */\n')
    f.write('window.LE=' + json.dumps(meta, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('le.js', os.path.getsize(f'{OUT}/data/le.js') // 1024, 'KB')

# ---- skill cards: the ability card of lastepochtools, reduced to a whitelist of tags and classes ----
KEEP = {'separator', 'ability-description', 'ability-params', 'with-divider', 'ability-alt-text', 'stat-value', 'mod-value',
        'ability-param-group', 'stat-extra', 'attr-scaling', 'attr-scaling-stats', 'attr-scaling-stat', 'mod-value-wrap',
        'ability-tags', 'ability-tag', 'bottom-block', 'ability-source-class', 'is-not-hit', 'middle-block', 'top-block',
        'ability-description-block', 'ability-name-sub', 'sub-ability', 'ability-sub-extra', 'damage-extra', 'level-scaling-stat',
        'buff', 'negative', 'positive', 'is-hit', 'stat-text'}
TAGS = {'div', 'span', 'br', 'ul', 'li', 'b', 'i'}
DROP = {'ability-bitmap-container', 'ability-name', 'view-invocations-block', 'ability-icon-inline', 'ailment-icon-inline', 'icons'}
class Clean(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.out = []; s.stack = []; s.skip = 0
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); cl = (a.get('class') or '').split()
        if s.skip or any(c in DROP for c in cl):
            if tag != 'br': s.skip += 1; s.stack.append(('skip', tag))
            return
        if tag == 'a':                                   # links to other pages of the site: kept as highlighted words
            s.out.append('<span class="lnk">'); s.stack.append(('tag', 'span')); return
        if tag not in TAGS:
            if tag != 'br': s.stack.append(('none', tag))
            return
        keep = [c for c in cl if c in KEEP]
        if tag == 'div' and 'ability-param-group' in keep and a.get('style'): keep.append('sub')
        if 'color:#FFF' in (a.get('style') or ''): keep.append('hl')
        if tag == 'br': s.out.append('<br>'); return
        s.out.append(f'<{tag}' + (f' class="{" ".join(keep)}"' if keep else '') + '>')
        s.stack.append(('tag', tag))
    def handle_endtag(s, tag):
        if tag == 'br' or not s.stack: return
        kind, t = s.stack.pop()
        if kind == 'skip': s.skip -= 1
        elif kind == 'tag': s.out.append(f'</{t}>')
    def handle_data(s, d):
        if not s.skip: s.out.append(html.escape(d, quote=False))
# lastepochtools prints the Cold damage type as "Золото" (gold) in Russian base damage lines
FIXES = {'ru': [(r'(<div>|, )Золото(: <span class="mod-value">)', r'\g<1>Холод\g<2>')]}
def clean(h):
    p = Clean(); p.feed(h); p.close()
    return ''.join(p.out).replace('<div class="ability-description-block"></div>', '')
for l in LANGS:
    fn = f'cards/{l}.json'
    if not os.path.exists(fn): print('no cards for', l); continue
    cards = json.load(open(fn, encoding='utf-8'))
    out = {i: clean(h) for i, h in cards.items() if h}
    for i, h in out.items():                  # known slips in the source translations
        for bad, good in FIXES.get(l, []): h = re.sub(bad, good, h)
        out[i] = h
    with open(f'{OUT}/data/skills/{l}.js', 'w', encoding='utf-8') as f:
        f.write('/* Skill cards (' + l + ') from lastepochtools.com, ' + DATA_VERSION + '. */\n')
        f.write('(window.LESK=window.LESK||{})[' + json.dumps(l) + ']=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(l, len(out), os.path.getsize(f'{OUT}/data/skills/{l}.js') // 1024, 'KB')
