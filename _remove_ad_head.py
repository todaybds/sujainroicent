"""
일시 비활성화: 모든 HTML에서 GTM + GA4 + Meta Pixel head script 통째로 제거
+ body 첫 부분의 GTM noscript도 제거
- 사이트 정상 동작 확인 후 신중히 재삽입
"""
import re, glob

# head 영역 4 블록
GTM_BLOCK = re.compile(
    r'\s*<!-- Google Tag Manager -->\s*\n'
    r'\s*<script>[\s\S]*?</script>\s*\n'
    r'\s*<!-- End Google Tag Manager -->\s*\n',
)
GA4_BLOCK = re.compile(
    r'\s*<!-- Google tag \(gtag\.js\)[^\n]*\n'
    r'\s*<script async src="https://www\.googletagmanager\.com/gtag/js[^"]*"></script>\s*\n'
    r'\s*<script>\s*\n[\s\S]*?gtag\(\'config\'[^\n]*\n\s*</script>\s*\n',
)
META_BLOCK = re.compile(
    r'\s*<!-- Meta Pixel Code -->\s*\n'
    r'\s*<script>\s*\n[\s\S]*?fbq\(\'track\',\s*\'PageView\'\);\s*\n\s*</script>'
    r'(\s*<!-- End Meta Pixel Code -->)?\s*\n?',
)
GTM_NOSCRIPT = re.compile(
    r'\s*<!-- Google Tag Manager \(noscript\) -->\s*\n'
    r'\s*<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html[^>]*"\s*\n'
    r'\s*[^>]*></iframe></noscript>\s*\n'
    r'\s*<!-- End Google Tag Manager \(noscript\) -->\s*\n',
)

targets = []
for p in ['*.htm', '*.html', 'mobile/*.htm', 'mobile/*.html']:
    targets.extend(glob.glob(p))
targets = [t for t in targets if '_bak_' not in t and not t.startswith('.')]

stats = {'gtm':0, 'ga4':0, 'meta':0, 'gtm_ns':0}
for path in targets:
    c = open(path, encoding='utf-8').read()
    new = c
    new, n = GTM_BLOCK.subn('\n', new); stats['gtm'] += n
    new, n = GA4_BLOCK.subn('\n', new); stats['ga4'] += n
    new, n = META_BLOCK.subn('\n', new); stats['meta'] += n
    new, n = GTM_NOSCRIPT.subn('\n', new); stats['gtm_ns'] += n
    if new != c:
        open(path, 'w', encoding='utf-8').write(new)

print(stats)
