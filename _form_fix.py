#!/usr/bin/env python3
"""Fix customer form: phone (010 fixed + numbers only) + interest type (84/101 only)."""
import re
from pathlib import Path

p = Path('board/bbs/write.php.html')
html = p.read_text(encoding='utf-8')

# 1. Replace phone select+inputs (lines around <select name="hp1">)
phone_old = re.compile(
    r'<select name="hp1" id="hp1" class="mnum">.*?</select>\s*'
    r'<em>-</em>\s*'
    r'<input type="number" pattern="\\d\*" name="hp2" id="hp2"[^>]*>\s*'
    r'<em>-</em>\s*'
    r'<input type="number" pattern="\\d\*" name="hp3" id="hp3"[^>]*>',
    re.DOTALL
)
phone_new = (
    '<input type="text" id="hp1_display" value="010" readonly class="hp_fixed">\n'
    '\t\t\t\t\t\t\t\t<input type="hidden" name="hp1" id="hp1" value="010">\n'
    '\t\t\t\t\t\t\t\t<em>-</em>\n'
    '\t\t\t\t\t\t\t\t<input type="text" name="hp2" id="hp2" value="" maxlength="4" inputmode="numeric" '
    'oninput="this.value=this.value.replace(/[^0-9]/g,\'\').slice(0,4)" placeholder="0000">\n'
    '\t\t\t\t\t\t\t\t<em>-</em>\n'
    '\t\t\t\t\t\t\t\t<input type="text" name="hp3" id="hp3" value="" maxlength="4" inputmode="numeric" '
    'oninput="this.value=this.value.replace(/[^0-9]/g,\'\').slice(0,4)" placeholder="0000">'
)
html, n1 = phone_old.subn(phone_new, html)
print(f'Phone: {n1} replacement(s)')

# 2. Replace interest type checkboxes (5 → 2)
unit_old = re.compile(
    r'<div class="unit_chk">\s*'
    r'<span><input type="checkbox" name="wr_5\[\]" id="wr_5_1" value="84A">.*?'
    r'<span><input type="checkbox" name="wr_5\[\]" id="wr_5_5" value="101"><label for="wr_5_5">101</label></span>\s*'
    r'</div>',
    re.DOTALL
)
unit_new = (
    '<div class="unit_chk">\n'
    '\t\t\t\t\t\t\t\t<span><input type="checkbox" name="wr_5[]" id="wr_5_1" value="84㎡"><label for="wr_5_1">84㎡</label></span>\n'
    '\t\t\t\t\t\t\t\t<span><input type="checkbox" name="wr_5[]" id="wr_5_2" value="101㎡"><label for="wr_5_2">101㎡</label></span>\n'
    '\t\t\t\t\t\t\t</div>'
)
html, n2 = unit_old.subn(unit_new, html)
print(f'Unit chk: {n2} replacement(s)')

p.write_text(html, encoding='utf-8')
print('Done.')
