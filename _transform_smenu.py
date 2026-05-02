#!/usr/bin/env python3
"""Flatten smenu HTML structure across PC sub-pages.

OLD:
  <ul>
    <a class="home"><img></a>                       <- orphan, invalid HTML
    <li class="smenu_depth1"><a>홈으로</a></li>
    <li class="smenu_depth1">                       <- wrapper containing all menus
      <ul>
        <li><a>사업안내</a><ul class="smenu_depth2">...</ul></li>
        ...
      </ul>
    </li>
  </ul>

NEW:
  <ul>
    <li class="home"><a><img></a></li>
    <li class="smenu_depth1 no_drop"><a>홈으로</a></li>
    <li class="smenu_depth1"><a>사업안내</a><ul class="smenu_depth2">...</ul></li>
    ...
    <li class="smenu_depth1 no_drop"><a>관심고객등록</a></li>
  </ul>

Notes
-----
HTML comments may contain `<ul>` / `<li>` tokens (e.g. commented-out menu items).
All depth-tracking loops below skip the entire `<!-- ... -->` block so that
counts stay correct.
"""

import re
import sys
from pathlib import Path


COMMENT_OPEN = '<!--'
COMMENT_CLOSE = '-->'


def skip_comment(html: str, i: int) -> int:
    """If `i` points at `<!--`, return the index right after the matching `-->`.
    Otherwise return -1."""
    if html.startswith(COMMENT_OPEN, i):
        end = html.find(COMMENT_CLOSE, i + 4)
        if end == -1:
            return len(html)  # unterminated comment, swallow rest
        return end + 3
    return -1


def find_matching_close_ul(html: str, start: int) -> int:
    """Given the position right after an opening <ul>, return position of its matching </ul>.

    Comments are skipped entirely."""
    n = len(html)
    i = start
    depth = 1
    ul_open = re.compile(r'<ul\b[^>]*>')
    while i < n and depth > 0:
        c_skip = skip_comment(html, i)
        if c_skip != -1:
            i = c_skip
            continue
        m = ul_open.match(html, i)
        if m:
            depth += 1
            i = m.end()
            continue
        if html[i:i+5] == '</ul>':
            depth -= 1
            if depth == 0:
                return i
            i += 5
            continue
        i += 1
    return -1


def flatten_inner(inner: str) -> str:
    """Add class='smenu_depth1' to top-level <li> tags inside the wrapper's <ul>.

    Top-level means li at depth 0 of nested <ul>s within `inner`. Comments are skipped."""
    out = []
    depth = 0
    pos = 0
    n = len(inner)
    tok_re = re.compile(r'<ul\b[^>]*>|</ul>|<li\b[^>]*>')
    while pos < n:
        c_skip = skip_comment(inner, pos)
        if c_skip != -1:
            out.append(inner[pos:c_skip])
            pos = c_skip
            continue
        m = tok_re.match(inner, pos)
        if not m:
            out.append(inner[pos])
            pos += 1
            continue
        t = m.group(0)
        if t.startswith('<ul'):
            out.append(t)
            depth += 1
        elif t == '</ul>':
            depth -= 1
            out.append(t)
        else:  # <li ...>
            if depth == 0:
                if 'class=' in t:
                    new_t = re.sub(r'class="([^"]*)"', r'class="smenu_depth1 \1"', t, count=1)
                else:
                    new_t = re.sub(r'<li\b', '<li class="smenu_depth1"', t, count=1)
                out.append(new_t)
            else:
                out.append(t)
        pos = m.end()
    return ''.join(out)


def add_no_drop(html: str) -> str:
    """Add 'no_drop' class to top-level <li class='smenu_depth1'> that don't contain smenu_depth2."""
    result = []
    i = 0
    n = len(html)
    open_re = re.compile(r'<li class="smenu_depth1">')
    ul_open = re.compile(r'<ul\b[^>]*>')
    li_open = re.compile(r'<li\b[^>]*>')
    while i < n:
        m = open_re.match(html, i)
        if not m:
            result.append(html[i])
            i += 1
            continue
        i = m.end()
        content_start = i
        depth = 1
        has_depth2 = False
        while i < n and depth > 0:
            c_skip = skip_comment(html, i)
            if c_skip != -1:
                i = c_skip
                continue
            ul_m = ul_open.match(html, i)
            if ul_m:
                if 'smenu_depth2' in ul_m.group(0):
                    has_depth2 = True
                i = ul_m.end()
                continue
            if html[i:i+5] == '</ul>':
                i += 5
                continue
            li_m = li_open.match(html, i)
            if li_m:
                depth += 1
                i = li_m.end()
                continue
            if html[i:i+5] == '</li>':
                depth -= 1
                if depth == 0:
                    break
                i += 5
                continue
            i += 1
        body = html[content_start:i]
        if has_depth2:
            result.append('<li class="smenu_depth1">')
        else:
            result.append('<li class="smenu_depth1 no_drop">')
        result.append(body)
        result.append('</li>')
        i += 5
    return ''.join(result)


def transform(html: str) -> str:
    # 1) Wrap orphan <a class="home"> in <li class="home">
    html = re.sub(
        r'<a\s+href="index\.htm"\s+class="home">\s*<img\s+src="image/icon_home\.png">\s*</a>',
        '<li class="home"><a href="index.htm"><img src="image/icon_home.png"></a></li>',
        html, count=1, flags=re.DOTALL
    )

    # 2) Find wrapper <li class="smenu_depth1"> followed by <ul>
    wrapper_open_re = re.compile(r'<li class="smenu_depth1">\s*<ul>')
    m = wrapper_open_re.search(html)
    if m is None:
        return html

    wrapper_start = m.start()
    inner_start = m.end()

    close_ul_pos = find_matching_close_ul(html, inner_start)
    if close_ul_pos < 0:
        return html

    inner_content = html[inner_start:close_ul_pos]

    after_ul = close_ul_pos + 5
    tail_match = re.match(r'\s*</li>', html[after_ul:])
    if not tail_match:
        return html

    wrapper_end = after_ul + tail_match.end()

    flat = flatten_inner(inner_content)
    html = html[:wrapper_start] + flat + html[wrapper_end:]

    # 3) Add no_drop class to top-level li without smenu_depth2 (e.g. 홈으로, 관심고객등록)
    html = add_no_drop(html)

    return html


def main():
    if len(sys.argv) < 2:
        print('Usage: transform_smenu.py <files...>', file=sys.stderr)
        sys.exit(1)
    changed = 0
    skipped = 0
    for fp in sys.argv[1:]:
        p = Path(fp)
        if not p.exists():
            print(f'NOT FOUND: {fp}')
            continue
        c = p.read_text(encoding='utf-8')
        nc = transform(c)
        if nc != c:
            p.write_text(nc, encoding='utf-8')
            print(f'OK    {fp}')
            changed += 1
        else:
            print(f'SKIP  {fp}')
            skipped += 1
    print(f'\nDone. changed={changed} skipped={skipped}')


if __name__ == '__main__':
    main()
