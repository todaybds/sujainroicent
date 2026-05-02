/*
 * smenu Breadcrumb Builder (PC sub-pages)
 *
 * Reads the existing .smenu structure on each PC sub-page and rewrites it as a
 * 2-level breadcrumb that mirrors the mobile sub-page header:
 *
 *   [Home Icon] | [Current Category ▼] | [Current Sub-page ▼]
 *
 * Where:
 *   Current Category dropdown lists ALL categories (jump to other categories)
 *   Current Sub-page dropdown lists sibling sub-pages within the current category
 *
 * Behavior:
 *   - Current URL is read from window.location (no hardcoded filename per page)
 *   - normalizeUrl() handles _check / noticeXX / digit-underscore stripping so
 *     pages like reservation01_check.html match reservation entries.
 *   - If the current URL matches no menu entry, the original .smenu is left as-is.
 *   - If the matching item is a top-level (.no_drop) link such as customer.html,
 *     only the category breadcrumb is rendered (no sub-page step).
 *
 * Drop-in replacement for the per-page inline filter script that previously
 * removed all non-matching .smenu_depth1 items.
 */
(function () {
  function normalizeUrl(url) {
    if (!url) return '';
    url = String(url).split('?')[0].split('#')[0];
    url = url.split('/').pop();
    url = url.replace(/_check/g, '');
    url = url.replace(/notice(\d+)/g, 'notice_NUM_$1');
    // Strip "-1", "-2", "-3" variants so magam-1.html matches magam.html, etc.
    url = url.replace(/-\d+(?=\.|$)/g, '');
    url = url.replace(/[\d_]+/g, '');
    return url;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function buildLi(item, hasDropdown, dropdownItems) {
    var cls = 'smenu_depth1' + (hasDropdown ? '' : ' no_drop');
    var html = '<li class="' + cls + '"><a href="' + escapeHtml(item.href || '#') + '">' + escapeHtml(item.name) + '</a>';
    if (hasDropdown && dropdownItems && dropdownItems.length) {
      html += '<ul class="smenu_depth2">';
      dropdownItems.forEach(function (d) {
        html += '<li><a href="' + escapeHtml(d.href) + '">' + escapeHtml(d.name) + '</a></li>';
      });
      html += '</ul>';
    }
    html += '</li>';
    return html;
  }

  function init() {
    if (typeof window.jQuery === 'undefined') return;
    var $ = window.jQuery;
    var $smenu = $('.smenu').first();
    if (!$smenu.length) return;
    var $ul = $smenu.find('> .rel_wrap > ul, > ul').first();
    if (!$ul.length) return;

    var currentUrl = normalizeUrl(window.location.pathname || '');

    // Snapshot of categories (top-level items) before any modification
    var categoriesData = [];
    $ul.children('.smenu_depth1').each(function () {
      var $cat = $(this);
      var $catLink = $cat.children('a').first();
      var subItems = [];
      $cat.find('> .smenu_depth2 > li > a').each(function () {
        subItems.push({
          name: $(this).text().trim(),
          href: $(this).attr('href') || '#'
        });
      });
      categoriesData.push({
        name: $catLink.text().trim(),
        href: $catLink.attr('href') || '#',
        subs: subItems
      });
    });

    if (!categoriesData.length) return;

    // Find current category & sub-page
    var matchedCategoryIndex = -1;
    var matchedSubIndex = -1;
    categoriesData.forEach(function (cat, ci) {
      // First check sub-pages
      cat.subs.forEach(function (sub, si) {
        if (normalizeUrl(decodeURIComponent(sub.href)) === currentUrl) {
          matchedCategoryIndex = ci;
          matchedSubIndex = si;
        }
      });
      // If category top link itself matches (no_drop categories like 관심고객등록)
      if (matchedCategoryIndex === -1 && normalizeUrl(decodeURIComponent(cat.href)) === currentUrl) {
        matchedCategoryIndex = ci;
      }
    });

    if (matchedCategoryIndex === -1) {
      // No match — leave original smenu intact (graceful fallback)
      return;
    }

    var currentCategory = categoriesData[matchedCategoryIndex];

    // Build category dropdown items (all OTHER categories — exclude self for cleanliness,
    // but include self as the visible label)
    // We include ALL categories so the user can jump from category dropdown.
    var categoryDropdownItems = categoriesData.map(function (c) {
      // For categories with sub-pages, link to first sub-page so user lands on a real page
      var primary = (c.subs && c.subs.length) ? c.subs[0] : c;
      return { name: c.name, href: primary.href };
    });

    // Build sub-page step (only if matched sub exists)
    var subStepHtml = '';
    if (matchedSubIndex !== -1 && currentCategory.subs.length > 0) {
      var currentSub = currentCategory.subs[matchedSubIndex];
      // Sub dropdown: all siblings (including self for clarity)
      subStepHtml = buildLi(
        { name: currentSub.name, href: currentSub.href },
        currentCategory.subs.length > 1,
        currentCategory.subs
      );
    }

    // Build category step
    var categoryStepHtml = buildLi(
      { name: currentCategory.name, href: (currentCategory.subs[0] || currentCategory).href },
      categoryDropdownItems.length > 1,
      categoryDropdownItems
    );

    // Replace ul content while preserving home icon
    var $home = $ul.children('.home').detach();
    $ul.empty();
    if ($home.length) $ul.append($home);
    $ul.append(categoryStepHtml);
    if (subStepHtml) $ul.append(subStepHtml);
  }

  if (typeof window.jQuery !== 'undefined') {
    window.jQuery(init);
  } else {
    // Defer until jQuery is loaded
    document.addEventListener('DOMContentLoaded', function () {
      if (typeof window.jQuery !== 'undefined') init();
    });
  }
})();
