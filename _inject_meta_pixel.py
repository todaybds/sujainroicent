"""
Meta Pixel 일괄 삽입 스크립트 (1회성, 보존)

대상: 루트 *.htm/*.html + mobile/*.htm/*.html
규칙:
- head 안 (</head> 직전): Meta Pixel 메인 스니펫 (init + PageView)
- 이미 1988984025053531가 들어있는 파일은 skip (멱등성)
"""
import re
import glob

PIXEL_ID = "1988984025053531"

HEAD_SNIPPET = f"""  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{PIXEL_ID}');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1"
  /></noscript>
  <!-- End Meta Pixel Code -->
"""

targets = []
for pattern in ['*.htm', '*.html', 'mobile/*.htm', 'mobile/*.html']:
    targets.extend(glob.glob(pattern))
targets = [t for t in targets if '_bak_' not in t and not t.startswith('.')]

skipped, modified, errors = [], [], []

for path in targets:
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()

        if PIXEL_ID in content:
            skipped.append(path)
            continue

        if '</head>' not in content:
            errors.append(f"{path}: no </head>")
            continue

        new_content = content.replace('</head>', HEAD_SNIPPET + '</head>', 1)

        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(new_content)
        modified.append(path)
    except Exception as e:
        errors.append(f"{path}: {e}")

print(f"modified: {len(modified)}")
print(f"skipped (already has Pixel): {len(skipped)}")
print(f"errors: {len(errors)}")
for e in errors:
    print(f"  {e}")
