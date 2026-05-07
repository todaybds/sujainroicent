import glob, re, os

files = sorted(glob.glob('*.htm') + glob.glob('*.html') + glob.glob('mobile/*.htm') + glob.glob('mobile/*.html'))
files = [f for f in files if not ('_bak_' in f or '.bak' in f or 'before-popup' in f or 'before-sec06' in f)]

print(f'== 전수 점검: {len(files)}개\n')

# 메인 페이지 (4개) 상세
mains = ['index.htm', 'mobile/index.html']
for f in mains:
    if not os.path.exists(f):
        continue
    print(f'==== [{f}] 상세 ====')
    c = open(f, encoding='utf-8').read()
    title = re.search(r'<title>([^<]+)</title>', c)
    desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
    keywords = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', c)
    canon = re.search(r'rel="canonical"\s+href="([^"]+)"', c)
    h1s = re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', c)
    h1s_clean = [re.sub(r'<[^>]+>', '', h).strip()[:80] for h in h1s]
    ogtitle = re.search(r'og:title"\s+content="([^"]+)"', c)
    ogdesc = re.search(r'og:description"\s+content="([^"]+)"', c)
    ogimg = re.search(r'og:image"\s+content="([^"]+)"', c)
    ogtype = re.search(r'og:type"\s+content="([^"]+)"', c)
    ogurl = re.search(r'og:url"\s+content="([^"]+)"', c)
    ogsitename = re.search(r'og:site_name"\s+content="([^"]+)"', c)
    twcard = re.search(r'twitter:card"\s+content="([^"]+)"', c)

    t = title.group(1) if title else None
    print(f'  title({len(t) if t else 0}자, 권장 30~60): {t or "(없음)"}')
    d = desc.group(1) if desc else None
    print(f'  description({len(d) if d else 0}자, 권장 120~160): {(d or "(없음)")[:130]}...')
    print(f'  keywords: {(keywords.group(1) if keywords else "(없음)")[:100]}')
    print(f'  canonical: {canon.group(1) if canon else "(없음)"}')
    print(f'  H1 태그 {len(h1s)}개:')
    for h in h1s_clean[:5]:
        print(f'    - "{h}"')
    print(f'  og:title: {ogtitle.group(1) if ogtitle else "(없음)"}')
    print(f'  og:desc:  {(ogdesc.group(1) if ogdesc else "(없음)")[:100]}...')
    print(f'  og:image: {ogimg.group(1) if ogimg else "(없음)"}')
    print(f'  og:type:  {ogtype.group(1) if ogtype else "(없음)"}')
    print(f'  og:url:   {ogurl.group(1) if ogurl else "(없음)"}')
    print(f'  og:site_name: {ogsitename.group(1) if ogsitename else "(없음)"}')
    print(f'  twitter:card: {twcard.group(1) if twcard else "(없음)"}')
    print()

# 전체 페이지 이슈 카운트
print('==== 전체 이슈 집계 ====')
issues = {
    'title_없음': [], 'title_너무짧음(<20)': [], 'title_너무김(>70)': [],
    'desc_없음': [], 'desc_너무짧음(<80)': [], 'desc_너무김(>180)': [],
    'h1_없음': [], 'h1_여러개': [],
    'canonical_없음': [], 'ogimg_없음': [],
    'description_중복': {}, 'title_중복': {},
}
for f in files:
    c = open(f, encoding='utf-8').read()
    title = re.search(r'<title>([^<]+)</title>', c)
    desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
    canon = re.search(r'rel="canonical"\s+href="([^"]+)"', c)
    h1s = re.findall(r'<h1[^>]*>[\s\S]*?</h1>', c)
    ogimg = re.search(r'og:image"\s+content="([^"]+)"', c)
    if not title:
        issues['title_없음'].append(f)
    else:
        t = title.group(1).strip()
        if len(t) < 20: issues['title_너무짧음(<20)'].append(f'{f}({len(t)})')
        if len(t) > 70: issues['title_너무김(>70)'].append(f'{f}({len(t)})')
        issues['title_중복'].setdefault(t, []).append(f)
    if not desc:
        issues['desc_없음'].append(f)
    else:
        d = desc.group(1).strip()
        if len(d) < 80: issues['desc_너무짧음(<80)'].append(f'{f}({len(d)})')
        if len(d) > 180: issues['desc_너무김(>180)'].append(f'{f}({len(d)})')
        issues['description_중복'].setdefault(d, []).append(f)
    if not h1s:
        issues['h1_없음'].append(f)
    elif len(h1s) > 1:
        issues['h1_여러개'].append(f'{f}({len(h1s)})')
    if not canon: issues['canonical_없음'].append(f)
    if not ogimg: issues['ogimg_없음'].append(f)

# 중복 발생만 표시
title_dupes = {k:v for k,v in issues['title_중복'].items() if len(v) > 1}
desc_dupes = {k:v for k,v in issues['description_중복'].items() if len(v) > 1}

for key in ['title_없음','title_너무짧음(<20)','title_너무김(>70)','desc_없음','desc_너무짧음(<80)','desc_너무김(>180)','h1_없음','h1_여러개','canonical_없음','ogimg_없음']:
    v = issues[key]
    flag = '✓' if not v else '!'
    print(f'  {flag} {key}: {len(v)}건')
    if v and len(v) <= 5:
        for x in v:
            print(f'      {x}')
    elif v:
        for x in v[:3]:
            print(f'      {x}')
        print(f'      ...외 {len(v)-3}건')

print(f'\n  ! title 중복(여러 페이지에 같은 title): {len(title_dupes)}건')
for t, fs in list(title_dupes.items())[:5]:
    print(f'      "{t[:60]}..." ({len(fs)}개): {fs[:3]}')

print(f'\n  ! description 중복: {len(desc_dupes)}건')
for d, fs in list(desc_dupes.items())[:5]:
    print(f'      "{d[:60]}..." ({len(fs)}개): {fs[:3]}')
