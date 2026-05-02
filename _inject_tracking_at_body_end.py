"""
광고추적(GTM+GA4+Meta Pixel) + antifraud.js를 body 끝(</body> 직전)에 재활성.
fullPage/jQuery init과 충돌 없도록 마지막에 로드.

- body 시작 직후: GTM noscript iframe (HTML 표준)
- </body> 직전: GTM script + GA4 + Meta Pixel + antifraud.js
"""
import re, glob

GTM_ID = "GTM-TDJXMMFD"
GA4_ID = "G-4BL7NCS5DG"
PIXEL_ID = "1988984025053531"

GTM_NOSCRIPT = f"""  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
"""

BODY_END = f"""  <!-- Google Tag Manager -->
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
  <!-- Meta Pixel Code -->
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
  <!-- End Meta Pixel Code -->
  <!-- antifraud -->
  <script src="/js/antifraud.js" async></script>
"""

targets = []
for p in ['*.htm', '*.html', 'mobile/*.htm', 'mobile/*.html']:
    targets.extend(glob.glob(p))
targets = [t for t in targets if '_bak_' not in t and not t.startswith('.')]

modified, skipped = 0, 0
for path in targets:
    c = open(path, encoding='utf-8').read()
    if GTM_ID in c:
        skipped.append(path) if isinstance(skipped, list) else None
        skipped += 1
        continue
    new = c
    # body 시작 직후 GTM noscript
    new, n1 = re.subn(r'(<body[^>]*>)', r'\1\n' + GTM_NOSCRIPT, new, count=1)
    # </body> 직전 광고 추적 + antifraud
    if '</body>' in new:
        new = new.replace('</body>', BODY_END + '</body>', 1)
    if new != c:
        open(path, 'w', encoding='utf-8').write(new)
        modified += 1

print(f'modified: {modified}, skipped: {skipped}')
