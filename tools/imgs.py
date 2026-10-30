import re, os, sys, glob, html, urllib.request
from bs4 import BeautifulSoup
RAW, OUT = sys.argv[1], sys.argv[2]; ok=fail=0
for f in sorted(glob.glob(f'{RAW}/blog__*.html')):
    slug = os.path.basename(f)[6:-5]
    body = BeautifulSoup(open(f).read(), 'html.parser').select_one('.w-richtext')
    for img in body.find_all('img'):
        src = img['src']; name = re.sub(r'[^A-Za-z0-9._-]', '_', html.unescape(src.split('/')[-1]).replace('%20','_'))
        d = f'{OUT}/public/images/blog/{slug}'; os.makedirs(d, exist_ok=True)
        p = f'{d}/{name}'
        if os.path.exists(p): ok+=1; continue
        try:
            with urllib.request.urlopen(urllib.request.Request(html.unescape(src), headers={'User-Agent':'Mozilla/5.0'}), timeout=60) as r: open(p,'wb').write(r.read()); ok+=1
        except Exception as e: fail+=1; print('FAIL', slug, src, e)
print('ok', ok, 'fail', fail)
