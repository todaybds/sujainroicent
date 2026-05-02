/*
 * Device-based auto-redirect between PC and mobile site.
 * - Viewport <= 768px on a PC page  -> redirects to /mobile/<page>
 * - Viewport >  768px on a mobile page -> redirects to /<page>
 * Only redirects pages that exist on BOTH sides (paired list below).
 * Special case: PC root uses index.htm, mobile uses index.html.
 * Re-evaluates on window resize (debounced).
 */
(function () {
  var BREAKPOINT = 768;
  var RESIZE_DEBOUNCE_MS = 250;

  // Filenames that exist on both PC and mobile (excluding index, handled separately)
  var paired = [
    'brand.html', 'community.html', 'complex.html', 'contract.html',
    'customer.html', 'document_capital.html',

    'interior.html', 'item_list.html', 'location.html',
    'magam.html', 'magam-1.html', 'magam-2.html', 'magam-3.html',
    'news.html', 'planning.html', 'premium.html',
    'reservation01.html', 'reservation01_check.html',
    'reservation02.html', 'reservation02_check.html',
    'reservation03.html', 'reservation03_check.html',
    'stampduty.html', 'supply.html', 'system.html',
    'unit.html', 'unit-1.html', 'unit-2.html', 'unit-3.html',
    'vr.html', 'vr-1.html', 'vr-2.html', 'vr-3.html'
  ];

  // Honor sticky manual override via ?view=pc / ?view=mobile
  var qs = location.search;
  if (qs.indexOf('view=pc') !== -1) {
    try { sessionStorage.setItem('forceView', 'pc'); } catch (e) {}
  } else if (qs.indexOf('view=mobile') !== -1) {
    try { sessionStorage.setItem('forceView', 'mobile'); } catch (e) {}
  }

  function getForced() {
    try { return sessionStorage.getItem('forceView'); } catch (e) { return null; }
  }

  function evaluate() {
    // Skip pages already converted to true responsive (marked with <meta name="responsive" content="true">)
    if (document.querySelector('meta[name="responsive"][content="true"]')) return;

    var path = location.pathname;
    var isMobilePath = path.indexOf('/mobile/') !== -1;

    var width = window.innerWidth || document.documentElement.clientWidth;
    var isMobileViewport = width <= BREAKPOINT;

    var forced = getForced();
    if (forced === 'pc') {
      isMobileViewport = false;
    } else if (forced === 'mobile') {
      isMobileViewport = true;
    }

    var m = path.match(/([^\/]+)$/);
    var filename = m ? m[1] : '';
    var isIndex = !filename || filename === 'index.htm' || filename === 'index.html';
    var hasPair = isIndex || paired.indexOf(filename) !== -1;
    if (!hasPair) return;

    if (!isMobilePath && isMobileViewport) {
      // PC -> mobile
      var basePath = path.substring(0, path.lastIndexOf('/') + 1);
      var mobileFile = isIndex ? 'index.html' : filename;
      location.replace(basePath + 'mobile/' + mobileFile + location.search + location.hash);
    } else if (isMobilePath && !isMobileViewport) {
      // mobile -> PC
      var pcBase = path.replace(/mobile\/[^\/]*$/, '');
      var pcFile = isIndex ? 'index.htm' : filename;
      location.replace(pcBase + pcFile + location.search + location.hash);
    }
  }

  // Initial check on load
  evaluate();

  // Re-check on resize (debounced) so swapping window size or rotating device transitions automatically
  var resizeTimer = null;
  window.addEventListener('resize', function () {
    if (resizeTimer) clearTimeout(resizeTimer);
    resizeTimer = setTimeout(evaluate, RESIZE_DEBOUNCE_MS);
  });

  // Some browsers fire orientationchange before resize settles
  window.addEventListener('orientationchange', function () {
    if (resizeTimer) clearTimeout(resizeTimer);
    resizeTimer = setTimeout(evaluate, RESIZE_DEBOUNCE_MS);
  });
})();
