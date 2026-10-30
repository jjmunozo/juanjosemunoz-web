import urllib.parse, re, os, sys, json, glob, html
from datetime import datetime
from bs4 import BeautifulSoup
from markdownify import markdownify as md
RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(f'{OUT}/src/content/blog', exist_ok=True)
# category map from category pages
cats = {}
catnames = {}
for f in glob.glob(f'{RAW}/categoria__*.html'):
    c = os.path.basename(f)[len('categoria__'):-5].split('?')[0]
    if c == 'todo': continue
    soup = BeautifulSoup(open(f).read(), 'html.parser')
    h = soup.find(['h1','h2']); catnames[c] = h.get_text(strip=True).capitalize() if h else c
    for a in soup.select('a[href^="/blog/"]'):
        cats.setdefault(a['href'][6:], set()).add(c)
images = set(); index = []
for f in sorted(glob.glob(f'{RAW}/blog__*.html')):
    slug = os.path.basename(f)[6:-5]
    soup = BeautifulSoup(open(f).read(), 'html.parser')
    title = soup.select_one('.blog-detail-header-wrap h1').get_text(strip=True)
    dtxt = soup.select_one('.cc-blog-date').get_text(strip=True)
    date = datetime.strptime(dtxt, '%B %d, %Y').date().isoformat()
    desc = soup.find('meta', attrs={'name':'description'})
    og = soup.find('meta', attrs={'property':'og:image'})
    body = soup.select_one('.w-richtext')
    for img in body.find_all('img'):
        src = img['src']; images.add(src)
        img['src'] = '/images/blog/' + slug + '/' + re.sub(r'[^A-Za-z0-9._-]', '_', html.unescape(src.split('/')[-1]).replace('%20','_'))
    embeds = []
    for fig in body.select('figure.w-richtext-figure-type-video'):
        ifr = fig.find('iframe'); src = html.unescape(ifr['src'])
        m = re.search(r'src=([^&]+)', src) if 'embedly' in src else None
        if m: src = urllib.parse.unquote(m.group(1))
        if src.startswith('//'): src = 'https:' + src
        embeds.append(f'<iframe src="{src}" loading="lazy" allowfullscreen style="width:100%;aspect-ratio:16/9;border:0"></iframe>')
        fig.replace_with(soup.new_string(f'EMBEDPLACEHOLDER{len(embeds)-1}X'))
    text = md(str(body), heading_style='ATX', bullets='-').replace('‍','')
    for i,e in enumerate(embeds): text = text.replace(f'EMBEDPLACEHOLDER{i}X', '\n\n'+e+'\n\n')
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    fm = {'title': title, 'date': date, 'slug': slug,
          'categories': sorted(cats.get(slug, [])),
          'description': desc['content'] if desc else '',
          'cover': og['content'] if og else ''}
    y = '---\n' + '\n'.join(f'{k}: {json.dumps(v, ensure_ascii=False)}' for k,v in fm.items()) + '\n---\n\n'
    open(f'{OUT}/src/content/blog/{slug}.md','w').write(y + text + '\n')
    index.append({**fm, 'words': len(text.split())})
json.dump(index, open(f'{OUT}/inventario-blog.json','w'), ensure_ascii=False, indent=1)
json.dump(sorted(images), open(f'{SPI}' if (SPI:=os.environ.get('IMGLIST')) else '/dev/null','w'), indent=1)
print(len(index), 'posts;', len(images), 'images;', 'categories:', catnames)
from collections import Counter
print(Counter(c for p in index for c in p['categories']), 'sin categoría:', sum(1 for p in index if not p['categories']))
print(Counter(p['date'][:4] for p in index))
