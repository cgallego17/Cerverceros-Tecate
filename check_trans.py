import re, glob, os

with open('locale/en/LC_MESSAGES/django.po', encoding='utf-8') as f:
    po = f.read()

# Extract all msgids (single and multiline)
po_msgids = set()
for m in re.finditer(r'msgid (\"[^\"]*\"(?:\s*\"[^\"]*\")*)', po, re.MULTILINE):
    raw = m.group(1)
    parts = re.findall(r'"([^"]*)"', raw)
    full = ''.join(parts)
    if full:
        po_msgids.add(full)

# Extract all trans strings from templates
missing = []
for path in sorted(glob.glob('templates/**/*.html', recursive=True)):
    try:
        with open(path, encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue
    fname = os.path.basename(path)
    for m in re.finditer(r'\{%-?\s+trans\s+[\"\'](.*?)[\"\']\s*-?%\}', content):
        s = m.group(1)
        if s and s not in po_msgids:
            missing.append((fname, s))

with open('_missing2.txt', 'w', encoding='utf-8') as out:
    seen = set()
    for fname, s in missing:
        key = (fname, s)
        if key not in seen:
            seen.add(key)
            out.write(fname + ' | ' + s + '\n')
    out.write('\nTotal faltantes: ' + str(len(seen)) + '\n')

print('Done. Total faltantes:', len(set(missing)))
