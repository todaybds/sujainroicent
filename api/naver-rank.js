// /api/naver-rank?kw=KEYWORD&domain=DOMAIN
// Vercel kr region IP에서 네이버 모바일 검색 → 우리 도메인 광고 순위 반환
// Cloudflare Worker가 호출 (한국 IP 우회용)

export const config = { runtime: 'edge', regions: ['icn1'] };  // 인천 region 강제

const UAs = [
  'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1',
  'Mozilla/5.0 (Linux; Android 14; SM-S928N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/123.0.6312.117 Mobile Safari/537.36',
  'Mozilla/5.0 (Linux; Android 14; SM-G998N Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36',
];

export default async function handler(req) {
  const url = new URL(req.url);
  const kw = url.searchParams.get('kw');
  const domain = url.searchParams.get('domain');
  const probe = parseInt(url.searchParams.get('probe') || '0', 10);
  if (!kw || !domain) return new Response(JSON.stringify({error:'missing kw/domain'}), {status:400});

  const ua = UAs[probe % UAs.length];
  const searchUrl = `https://m.search.naver.com/search.naver?where=m&query=${encodeURIComponent(kw)}`;
  try {
    const res = await fetch(searchUrl, {
      headers: {
        'User-Agent': ua,
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Cache-Control': 'no-cache',
      },
    });
    if (!res.ok) return Response.json({rank:null, reason:`http_${res.status}`, probe});
    const html = await res.text();

    // 도메인 출현 위치 → 직전 400자에서 r=N&i=nad- 추출
    const escD = domain.replace(/[.+*?^$(){}|[\]\\]/g, '\\$&');
    const domainRe = new RegExp(escD, 'gi');
    const ranks = [];
    let m;
    while ((m = domainRe.exec(html)) !== null) {
      const ctx = html.substring(Math.max(0, m.index - 400), m.index);
      const rm = ctx.match(/r=(\d+)&i=nad-[a-z0-9-]+/i);
      if (rm) {
        const r = parseInt(rm[1], 10);
        if (!isNaN(r) && r > 0 && r < 100) ranks.push(r);
      }
    }
    if (ranks.length === 0) {
      const hasAds = html.includes('nad-a001') || html.includes('pwl.tit') || html.includes('power_link');
      const hasDomain = html.toLowerCase().includes(domain.toLowerCase());
      return Response.json({rank:null, reason: hasAds ? (hasDomain ? 'domain_found_no_r' : 'not_in_ads') : 'no_pwl_section', probe, htmlLen: html.length});
    }
    return Response.json({rank: Math.min(...ranks), reason:'found', probe, count: ranks.length});
  } catch(e) {
    return Response.json({rank:null, reason:'fetch_err:'+String(e).substring(0,80), probe});
  }
}
