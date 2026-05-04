"""
보라웨어 부정클릭 차단 스크립트(protect_id=j764)를 모든 HTML(루트 + mobile/)
의 </body> 직전에 삽입. 기존 antifraud.js 라인 바로 위에 그룹지어 배치.
이미 삽입된 파일은 스킵 (idempotent).
"""
import glob, os

MARKER = 'BORAWARE LOG SCRIPT'
SNIPPET = """  <!-- BORAWARE LOG SCRIPT. -->
  <script type="text/javascript">
  var protect_id = 'j764';
  </script>
  <script async type="text/javascript" src="//script.boraware.kr/protect_script_v2.js"></script>
  <noscript><img src="//script.boraware.kr/protect_nbora.php?protect_id=j764" style="display:none;width:0;height:0;" border="0" /></noscript>
  <!-- END OF BORAWARE LOG SCRIPT -->
"""

ANCHOR_ANTIFRAUD = '<!-- antifraud -->'
ANCHOR_BODY_END = '</body>'

targets = []
for p in ['*.htm', '*.html', 'mobile/*.htm', 'mobile/*.html']:
    targets.extend(glob.glob(p))
targets = [t for t in targets if '_bak_' not in t and not os.path.basename(t).startswith('.')]

modified, skipped, no_anchor = 0, 0, []
for path in targets:
    c = open(path, encoding='utf-8').read()
    if MARKER in c:
        skipped += 1
        continue
    if ANCHOR_ANTIFRAUD in c:
        new = c.replace(ANCHOR_ANTIFRAUD, SNIPPET + '  ' + ANCHOR_ANTIFRAUD, 1)
    elif ANCHOR_BODY_END in c:
        new = c.replace(ANCHOR_BODY_END, SNIPPET + ANCHOR_BODY_END, 1)
    else:
        no_anchor.append(path)
        continue
    open(path, 'w', encoding='utf-8').write(new)
    modified += 1

print(f'modified: {modified}, skipped: {skipped}')
if no_anchor:
    print('no anchor (skipped):')
    for p in no_anchor:
        print(' -', p)
