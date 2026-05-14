import re

filepath = r"c:\Users\User\Documents\CERVECEROS DE TECATE\Cerverceros-Tecate\templates\equipo\inicio.html"

with open(filepath, encoding='utf-8') as f:
    content = f.read()

# Pattern: class="... lang-text ..." data-es="TEXT" data-en="TEXT2">TEXT</tag>
# Match: ... class="[classes] lang-text [more classes]" data-es="ES" data-en="EN"[optional attrs]>ES_CONTENT
pattern = re.compile(
    r'(<[^>]*?\s)class="([^"]*?)\s*lang-text\s*([^"]*?)"\s*data-es="([^"]*?)"\s*data-en="([^"]*?)"([^>]*)>([^<]*)',
    re.DOTALL
)

def do_replace(m):
    tag_start = m.group(1)
    pre_class = m.group(2)
    post_class = m.group(3)
    data_es = m.group(4)
    data_en = m.group(5)
    extra_attrs = m.group(6)
    _content = m.group(7)
    
    # Rebuild clean class attr (remove lang-text, strip extra spaces)
    clean_classes = (pre_class + ' ' + post_class).strip()
    if clean_classes:
        class_attr = f'class="{clean_classes}"'
    else:
        class_attr = ''
    
    # Rebuild tag
    if class_attr:
        new_tag = f'{tag_start}{class_attr}{extra_attrs}>{{% trans "{data_es}" %}}'
    else:
        new_tag = f'{tag_start.rstrip()}{extra_attrs}>{{% trans "{data_es}" %}}'
    return new_tag

new_content = pattern.sub(do_replace, content)

# Count replacements
count = len(re.findall(r'lang-text', content)) - len(re.findall(r'lang-text', new_content))
print(f"Replaced {count} lang-text occurrences")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")
