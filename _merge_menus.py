#!/usr/bin/env python3
"""Merge 계약안내 sub-pages into 분양안내 across PC and mobile menus.

NEW 분양안내 dropdown:
  - 공급안내 (supply.html)
  - 계약체결 안내 (contract.html)
  - 자금조달 계획서 (document_capital.html)
  - 인지세 안내 (stampduty.html)

REMOVED:
  - 계약안내 category entirely
  - 추가 선택품목 계약 안내문 (notice02.html) — file deleted separately
"""

import re
import sys
from pathlib import Path

# === New menu blocks ===

NEW_PC_HEADER = '''<li><a href="supply.html">분양안내</a>
            <ul class="header_menu_depth2">
              <li><a href="supply.html">공급안내</a></li>
              <li><a href="contract.html">계약체결 안내</a></li>
              <li><a href="document_capital.html">자금조달 계획서</a></li>
              <li><a href="stampduty.html">인지세 안내</a></li>
            </ul>
          </li>'''

NEW_PC_SMENU = '''<li class="smenu_depth1"><a href="supply.html">분양안내</a>
            <ul class="smenu_depth2">
              <li><a href="supply.html">공급안내</a></li>
              <li><a href="contract.html">계약체결 안내</a></li>
              <li><a href="document_capital.html">자금조달 계획서</a></li>
              <li><a href="stampduty.html">인지세 안내</a></li>
            </ul>
          </li>'''

NEW_MOBILE_NAV = '''<li>
            <span>분양안내</span>
            <ul class="sub">
              <li><a href="supply.html">공급안내</a></li>
              <li><a href="contract.html">계약체결 안내</a></li>
              <li><a href="document_capital.html">자금조달 계획서</a></li>
              <li><a href="stampduty.html">인지세 안내</a></li>
            </ul>
          </li>'''

NEW_MOBILE_SMENU_WRAP = '''<!-- 분양안내 -->
<div class="smenu_wrap">
  <ul>
    <li><a href="supply.html" class="sm_supply">공급안내</a></li>
    <li><a href="contract.html" class="sm_contract">계약체결 안내</a></li>
    <li><a href="document_capital.html" class="sm_document_capital">자금조달 계획서</a></li>
    <li><a href="stampduty.html" class="sm_stampduty">인지세 안내</a></li>
  </ul>
</div>'''

# === Patterns to replace ===

# PC header_menu_wrap: <li><a href="schedule.html">분양안내</a>...</li> + <li><a href="document_common.html">계약안내</a>...</li>
PC_HEADER_PATTERN = re.compile(
    r'<li><a href="schedule\.html">분양안내</a>\s*'
    r'<ul class="header_menu_depth2">.*?</ul>\s*'
    r'</li>\s*'
    r'<li><a href="document_common\.html">계약안내</a>\s*'
    r'<ul class="header_menu_depth2">.*?</ul>\s*'
    r'</li>',
    re.DOTALL
)

# PC smenu: similar but with smenu_depth1/smenu_depth2 classes
PC_SMENU_PATTERN = re.compile(
    r'<li class="smenu_depth1"><a href="schedule\.html">분양안내</a>\s*'
    r'<ul class="smenu_depth2">.*?</ul>\s*'
    r'</li>\s*'
    r'<li class="smenu_depth1"><a href="document_common\.html">계약안내</a>\s*'
    r'<ul class="smenu_depth2">.*?</ul>\s*'
    r'</li>',
    re.DOTALL
)

# Mobile nav (gnb): <li><span>분양안내</span>...</li> + <li><span>계약안내</span>...</li>
MOBILE_NAV_PATTERN = re.compile(
    r'<li>\s*<span>분양안내</span>\s*'
    r'<ul class="sub">.*?</ul>\s*'
    r'</li>\s*'
    r'<li>\s*<span>계약안내</span>\s*'
    r'<ul class="sub">.*?</ul>\s*'
    r'</li>',
    re.DOTALL
)

# Mobile sub-page: hea_drop 계약안내 li (remove)
MOBILE_HEA_DROP_CONTRACT = re.compile(
    r'\s*<li><a href="contract\.html">계약안내</a></li>'
)

# Mobile sub-page: 분양안내 smenu_wrap block (replace with merged version)
MOBILE_SMENU_BUNYANG = re.compile(
    r'<!-- 분양안내 -->\s*'
    r'<div class="smenu_wrap">\s*'
    r'<ul>.*?</ul>\s*'
    r'</div>',
    re.DOTALL
)

# Mobile sub-page: 계약안내 smenu_wrap block (remove entirely)
MOBILE_SMENU_GYEYAK = re.compile(
    r'\s*<!-- 계약안내 -->\s*'
    r'<div class="smenu_wrap">\s*'
    r'<ul>.*?</ul>\s*'
    r'</div>',
    re.DOTALL
)


def transform(html: str) -> tuple[str, list[str]]:
    """Apply all replacements. Returns (new_html, list_of_changes_made)."""
    changes = []
    new_html = html

    new_html, n = PC_HEADER_PATTERN.subn(NEW_PC_HEADER, new_html)
    if n > 0:
        changes.append(f'pc_header({n})')

    new_html, n = PC_SMENU_PATTERN.subn(NEW_PC_SMENU, new_html)
    if n > 0:
        changes.append(f'pc_smenu({n})')

    new_html, n = MOBILE_NAV_PATTERN.subn(NEW_MOBILE_NAV, new_html)
    if n > 0:
        changes.append(f'm_nav({n})')

    new_html, n = MOBILE_HEA_DROP_CONTRACT.subn('', new_html)
    if n > 0:
        changes.append(f'm_hea_drop({n})')

    new_html, n = MOBILE_SMENU_BUNYANG.subn(NEW_MOBILE_SMENU_WRAP, new_html)
    if n > 0:
        changes.append(f'm_smenu_bunyang({n})')

    new_html, n = MOBILE_SMENU_GYEYAK.subn('', new_html)
    if n > 0:
        changes.append(f'm_smenu_gyeyak({n})')

    return new_html, changes


def main():
    if len(sys.argv) < 2:
        print('Usage: _merge_menus.py <files...>', file=sys.stderr)
        sys.exit(1)
    changed = 0
    skipped = 0
    for fp in sys.argv[1:]:
        p = Path(fp)
        if not p.exists():
            print(f'NOT FOUND: {fp}')
            continue
        c = p.read_text(encoding='utf-8')
        nc, changes = transform(c)
        if nc != c:
            p.write_text(nc, encoding='utf-8')
            print(f'OK    {fp}  [{",".join(changes)}]')
            changed += 1
        else:
            print(f'SKIP  {fp}')
            skipped += 1
    print(f'\nDone. changed={changed} skipped={skipped}')


if __name__ == '__main__':
    main()
