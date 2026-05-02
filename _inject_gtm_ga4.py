"""
GTM + GA4 일괄 삽입 스크립트 (1회성, 보존)

대상: 루트 *.htm/*.html + mobile/*.htm/*.html
규칙:
- head 안 (</head> 직전): GTM 메인 스니펫 + GA4 gtag.js 둘 다
- body 시작 직후: GTM noscript iframe
- 이미 GTM-TDJXMMFD가 들어있는 파일은 skip (멱등성)
"""
import re
import glob
import os

GTM_ID = "GTM-TDJXMMFD"
GA4_ID = "G-4BL7NCS5DG"

HEAD_SNIPPET = f"""  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{GTM_ID}');</script>
  <!-- End Google Tag Manager -->
  <!-- Google tag (gtag.js) — GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}');
  </script>
"""

BODY_SNIPPET = f"""  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
"""

# 대상 파일
targets = []
for pattern in ['*.htm', '*.html', 'mobile/*.htm', 'mobile/*.html']:
    targets.extend(glob.glob(pattern))

# 백업/숨김 제외
targets = [t for t in targets if '_bak_' not in t and not t.startswith('.')]

skipped, modified, errors = [], [], []

for path in targets:
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()

        if GTM_ID in content:
            skipped.append(path)
            continue

        # head 안에 추가
        if '</head>' not in content:
            errors.append(f"{path}: no </head>")
            continue
        new_content = content.replace('</head>', HEAD_SNIPPET + '</head>', 1)

        # body 시작 직후에 noscript 추가
        new_content2, n = re.subn(r'(<body[^>]*>)', r'\1\n' + BODY_SNIPPET, new_content, count=1)
        if n == 0:
            errors.append(f"{path}: no <body>")
            continue

        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(new_content2)
        modified.append(path)
    except Exception as e:
        errors.append(f"{path}: {e}")

print(f"modified: {len(modified)}")
print(f"skipped (already has GTM): {len(skipped)}")
print(f"errors: {len(errors)}")
for e in errors:
    print(f"  {e}")
