"""
og:image 일괄 교체: thumb2.png → og_share.jpg (2000x949)
- og:image content URL 교체
- og:image:width 1920 → 2000
- og:image:height 1000 → 949
- og:image:alt 갱신 (조감도 → 단지 전경)
"""
import glob, re

OLD_URL = 'https://sujainroicent.com/meta/thumb2.png'
NEW_URL = 'https://sujainroicent.com/meta/og_share.jpg'
NEW_W = '2000'
NEW_H = '949'
NEW_ALT = '인하대역 수자인 로이센트 단지 전경'

files = sorted(glob.glob('*.htm') + glob.glob('*.html') + glob.glob('mobile/*.htm') + glob.glob('mobile/*.html'))
files = [f for f in files if not (
    '_bak_' in f or '.bak' in f or 'before-popup' in f or 'before-sec06' in f
)]

modified = 0
for path in files:
    c = open(path, encoding='utf-8').read()
    orig = c
    # og:image content URL
    c = c.replace(f'content="{OLD_URL}"', f'content="{NEW_URL}"')
    # og:image:width
    c = re.sub(r'(<meta\s+property="og:image:width"\s+content=")[^"]+(")', rf'\g<1>{NEW_W}\g<2>', c)
    # og:image:height
    c = re.sub(r'(<meta\s+property="og:image:height"\s+content=")[^"]+(")', rf'\g<1>{NEW_H}\g<2>', c)
    # og:image:alt
    c = re.sub(r'(<meta\s+property="og:image:alt"\s+content=")[^"]+(")', rf'\g<1>{NEW_ALT}\g<2>', c)
    if c != orig:
        open(path, 'w', encoding='utf-8').write(c)
        modified += 1

print(f'교체 완료: {modified}/{len(files)} 파일')
