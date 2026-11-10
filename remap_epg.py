import sys, gzip, re, xml.etree.ElementTree as ET
src, plids, out = sys.argv[1], sys.argv[2], sys.argv[3]
def key(x):
    x = x.lower().strip()
    x = re.sub(r'\.hd\.\.\d+', '', x)
    x = re.sub(r'\.it$', '', x)
    x = x.replace('hd', '')
    x = re.sub(r'[^a-z0-9]', '', x)
    return {'20': '20mediaset', 'mediaset20': '20mediaset', 'rainews': 'rainews24'}.get(x, x)
targets = {}
for line in open(plids, encoding='utf-8'):
    pid = line.strip()
    if pid: targets.setdefault(key(pid), set()).add(pid)
raw = open(src, 'rb').read()
try: raw = gzip.decompress(raw)
except OSError: pass
root = ET.fromstring(raw)
chans = root.findall('channel')
# per key prefer non-HD source channel
best = {}
for c in chans:
    cid = c.get('id'); k = key(cid)
    if k not in targets: continue
    hd = 'hd' in cid.lower()
    if k not in best or (best[k][1] and not hd): best[k] = (cid, hd)
chosen = {v[0]: k for k, v in best.items()}
new = ET.Element('tv', root.attrib)
n_ch = n_pr = 0
for c in chans:
    if c.get('id') not in chosen: continue
    for t in sorted(targets[chosen[c.get('id')]]):
        d = ET.fromstring(ET.tostring(c)); d.set('id', t); new.append(d); n_ch += 1
for p in root.findall('programme'):
    ch = p.get('channel')
    if ch not in chosen: continue
    for t in sorted(targets[chosen[ch]]):
        d = ET.fromstring(ET.tostring(p)); d.set('channel', t); new.append(d); n_pr += 1
ET.ElementTree(new).write(out, encoding='utf-8', xml_declaration=True)
print('source channels used:', len(chosen), '| channel entries:', n_ch, '| programmes:', n_pr)
print('mapped:', ', '.join(sorted(chosen)))
