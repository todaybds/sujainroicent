"""
수자인 메타 태그 일괄 보강
- title/og:title 중복 제거 (index 4개)
- og:type=mobile → website (모바일 39개)
- og:url 추가 (85개)
- og:image:width/height/alt 추가 (85개)
- og:site_name 추가 (85개)
- 모바일 canonical: PC 정본 URL 통일

backup 파일(_bak_, before-popup, .bak.before) 제외.
idempotent: 이미 보강된 항목은 skip.
"""
import glob, os, re

SITE = 'https://sujainroicent.com'
SITE_NAME = '인하대역 수자인 로이센트'
OG_IMG = 'https://sujainroicent.com/meta/thumb2.png'
OG_IMG_W = '1920'
OG_IMG_H = '1000'
OG_IMG_ALT = '인하대역 수자인 로이센트 조감도'

# PC 루트 = index.htm. 그 외 PC 페이지는 파일명 그대로.
def pc_url_for(path):
    """path: 'brand.html' or 'mobile/brand.html' → PC 정본 URL"""
    base = os.path.basename(path)
    if base in ('index.htm', 'index.html'):
        return SITE + '/'
    return SITE + '/' + base

def is_mobile(path):
    return path.startswith('mobile' + os.sep) or path.startswith('mobile/')

def patch_file(path):
    c = open(path, encoding='utf-8').read()
    orig = c
    changes = []

    # 1. title 중복 제거: "X - X - Y" → "X | Y"
    def fix_dup_title(text, tag_name):
        m = re.search(rf'<{tag_name}>([^<]+)</{tag_name}>' if tag_name=='title' else None, text) if tag_name=='title' else None
        return text
    # title
    m = re.search(r'<title>([^<]+)</title>', c)
    if m:
        t = m.group(1)
        parts = [p.strip() for p in t.split(' - ')]
        if len(parts) >= 2 and parts[0] == parts[1]:
            new_title = parts[0] + ' | ' + ' - '.join(parts[2:])
            c = c.replace(f'<title>{t}</title>', f'<title>{new_title}</title>', 1)
            changes.append(f'title 중복제거: {t[:50]}... → {new_title[:50]}')
    # og:title
    m = re.search(r'(<meta\s+property="og:title"\s+content=")([^"]+)(")', c)
    if m:
        ot = m.group(2)
        parts = [p.strip() for p in ot.split(' - ')]
        if len(parts) >= 2 and parts[0] == parts[1]:
            new_ot = parts[0] + ' | ' + ' - '.join(parts[2:])
            c = c.replace(m.group(0), m.group(1) + new_ot + m.group(3), 1)
            changes.append(f'og:title 중복제거')

    # 2. og:type mobile → website
    c2 = re.sub(r'(<meta\s+property="og:type"\s+content=")mobile(")', r'\1website\2', c)
    if c2 != c:
        changes.append('og:type mobile→website')
        c = c2

    # 3. canonical: 모바일은 PC 정본
    if is_mobile(path):
        target_canon = pc_url_for(path)
        m = re.search(r'(<link\s+rel="canonical"\s+href=")([^"]+)(")', c)
        if m and m.group(2) != target_canon:
            c = c.replace(m.group(0), m.group(1) + target_canon + m.group(3), 1)
            changes.append(f'mobile canonical → {target_canon}')

    # 4. og:url 추가 (canonical과 동일 = PC 정본 URL)
    if 'og:url' not in c:
        canon_url = pc_url_for(path)
        # og:image meta 위에 삽입
        og_url_tag = f'  <meta property="og:url" content="{canon_url}">\n'
        if '<meta property="og:image"' in c:
            c = c.replace('<meta property="og:image"', og_url_tag.lstrip() + '  <meta property="og:image"', 1)
            changes.append(f'og:url 추가 → {canon_url}')

    # 5. og:image 보조 메타 추가 (width/height/alt)
    if 'og:image:width' not in c:
        # og:image 다음 줄에 삽입
        m = re.search(r'(<meta\s+property="og:image"\s+content="[^"]+"\s*/?>)', c)
        if m:
            extra = (
                f'\n  <meta property="og:image:width" content="{OG_IMG_W}">'
                f'\n  <meta property="og:image:height" content="{OG_IMG_H}">'
                f'\n  <meta property="og:image:alt" content="{OG_IMG_ALT}">'
            )
            c = c.replace(m.group(1), m.group(1) + extra, 1)
            changes.append('og:image:width/height/alt 추가')

    # 6. og:site_name 추가
    if 'og:site_name' not in c:
        # og:type 다음에 삽입
        m = re.search(r'(<meta\s+property="og:type"\s+content="[^"]+"\s*/?>)', c)
        if m:
            tag = f'\n  <meta property="og:site_name" content="{SITE_NAME}">'
            c = c.replace(m.group(1), m.group(1) + tag, 1)
            changes.append('og:site_name 추가')

    if c != orig:
        open(path, 'w', encoding='utf-8').write(c)
        return changes
    return None


def main():
    files = sorted(glob.glob('*.htm') + glob.glob('*.html') + glob.glob('mobile/*.htm') + glob.glob('mobile/*.html'))
    # 백업 파일 제외
    files = [f for f in files if not (
        '_bak_' in f
        or '.bak' in f
        or 'before-popup' in f
        or 'before-sec06' in f
    )]

    total, modified = 0, 0
    for path in files:
        total += 1
        result = patch_file(path)
        if result:
            modified += 1
            print(f'[{path}]')
            for ch in result:
                print(f'  - {ch}')

    print(f'\n=== 총 {total}개 검사, {modified}개 수정 ===')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
