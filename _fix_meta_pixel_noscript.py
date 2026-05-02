"""
Meta Pixel noscript img가 head 안에 들어가서 brower가 body로 강제 이동시켜
layout 깨지는 문제 fix. 모든 HTML head에서 noscript 4줄 제거.

(noscript는 JS 비활성 사용자 backup인데, 우리 사이트는 JS 의존이라 사실상 무의미)
"""
import re
import glob

PATTERN = re.compile(
    r'\s*<noscript><img height="1" width="1" style="display:none"\s*\n'
    r'\s*src="https://www\.facebook\.com/tr\?id=\d+&ev=PageView&noscript=1"\s*\n'
    r'\s*/></noscript>\n',
    re.MULTILINE
)

targets = []
for p in ['*.htm', '*.html', 'mobile/*.htm', 'mobile/*.html']:
    targets.extend(glob.glob(p))
targets = [t for t in targets if '_bak_' not in t and not t.startswith('.')]

modified, skipped = 0, 0
for path in targets:
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    new = PATTERN.sub('', content)
    if new != content:
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(new)
        modified += 1
    else:
        skipped += 1

print(f"modified: {modified}, no-change: {skipped}")
