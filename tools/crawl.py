import re, sys, os, urllib.request, urllib.parse, time, json
OUT=sys.argv[1]; BASE='https://www.juanjosemunoz.com'
seen=set(); queue=['/']; results={}
def fetch(u):
    req=urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, r.read().decode('utf-8','replace')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return str(e), ''
while queue:
    p=queue.pop(0)
    if p in seen: continue
    seen.add(p)
    st,body=fetch(BASE+p); results[p]=st
    if body:
        fn=(p.strip('/').replace('/','__') or 'index')+'.html'
        open(os.path.join(OUT,fn),'w').write(body)
        for h in re.findall(r'href="([^"]+)"', body):
            u=urllib.parse.urlparse(h)
            if u.netloc in ('', 'www.juanjosemunoz.com', 'juanjosemunoz.com') and not h.startswith('#'):
                path=u.path or '/'
                if re.search(r'\.(png|jpe?g|css|js|svg|ico|pdf|webp|gif)$', path, re.I): continue
                if path not in seen: queue.append(path)
        # pagination links like ?xxxx_page=2
        for q in set(re.findall(r'href="(\?[^"]*page=\d+)"', body)):
            pp=p.split('?')[0]+html_q if False else p.split('?')[0]+q.replace('&amp;','&')
            if pp not in seen: queue.append(pp)
    time.sleep(0.2)
json.dump(results, open(os.path.join(OUT,'_status.json'),'w'), indent=1)
for k,v in sorted(results.items()): print(v,k)
