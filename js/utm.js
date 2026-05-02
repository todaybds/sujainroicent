// UTM 파라미터 localStorage + 쿠키 백업 저장 (모든 페이지 공통)
// - 최초 유입(first) UTM은 한 번만 저장하고 덮어쓰지 않음
// - 최종 유입(last) UTM은 매번 갱신하여 최신 채널도 추적 가능
// - 쿠키에도 first UTM 백업 (localStorage 삭제 대비)
(function() {
    var params = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'];
    var urlParams = new URLSearchParams(window.location.search);
    var hasUTM = params.some(function(p) { return urlParams.get(p); });
    if (!hasUTM) return;

    params.forEach(function(p) {
        var val = urlParams.get(p) || "";
        // 최초 유입 UTM: 이미 저장된 값이 없을 때만 기록
        if (!localStorage.getItem("first_" + p) && val) {
            localStorage.setItem("first_" + p, val);
        }
        // 최초 유입 UTM 쿠키 백업 (30일 유지)
        if (val && !document.cookie.match(new RegExp('(?:^|; )first_' + p + '='))) {
            document.cookie = 'first_' + p + '=' + encodeURIComponent(val) + ';max-age=2592000;path=/';
        }
        // 최종 유입 UTM: 항상 갱신
        if (val) {
            localStorage.setItem(p, val);
        }
    });
})();

// 관심고객등록 링크에 UTM 파라미터를 URL로 직접 전달 (localStorage 유실 대비)
(function() {
    var params = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content'];

    function getStoredUTM() {
        var result = {};
        var found = false;
        var urlParams = new URLSearchParams(window.location.search);
        params.forEach(function(p) {
            var val = urlParams.get(p) || localStorage.getItem(p) || localStorage.getItem("first_" + p) || "";
            if (!val) {
                var match = document.cookie.match(new RegExp('(?:^|; )first_' + p + '=([^;]*)'));
                if (match) val = decodeURIComponent(match[1]);
            }
            if (val) { result[p] = val; found = true; }
        });
        return found ? result : null;
    }

    var stored = getStoredUTM();
    if (!stored) return;

    var links = document.querySelectorAll('a[href*="wish/index"]');
    for (var i = 0; i < links.length; i++) {
        try {
            var url = new URL(links[i].href, window.location.origin);
            for (var key in stored) {
                if (!url.searchParams.has(key)) {
                    url.searchParams.set(key, stored[key]);
                }
            }
            links[i].href = url.pathname + url.search;
        } catch(e) {}
    }
})();
