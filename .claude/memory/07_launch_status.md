---
name: 라이브 준비 진행 상태
description: GitHub 푸시 + Vercel 배포 + 도메인 라이브 단계 진행 상태. 거의 모든 작업 완료, 잔여 항목은 카카오 채널 URL 1건만
type: project
---

# 라이브 준비 (2026-05-05 기준)

## 컨텍스트

이전 분양사이트 코드(`sujain-roicent.co.kr`)를 그대로 복사한 상태에서 새 분양으로 개편. **새 도메인 `sujainroicent.com`으로 라이브 완료**. GitHub 저장소: `https://github.com/todaybds/sujainroicent`. Vercel 배포: `https://sujainroicent.vercel.app` + 커스텀 도메인 `https://sujainroicent.com` 둘 다 200 OK.

참조 자료(바탕화면 형제 폴더):
- `cantaviledition.com/` — Vercel 라이브 사례
- `unjeong-ipark.com/` — 디자인 참조
- `부정클릭방지시스템/` — 자체 V20 시스템 (이번엔 사용 안 함, 보라웨어 상용 채택)
- `사이트_정리.txt` — 라이브 사이트 6개 URL 목록

## ✅ Phase 1 완료 (2026-04-29)

[02_modifications_log.md](02_modifications_log.md) 섹션 27 참조

- 이전 사이트 트래킹 ID 4종 완전 제거 (GTM-TGHF9M29 / AW-17370728994 / G-TNYYRLMMV8 / gtag/ 폴더)
- `.gitignore` + `vercel.json` 신규 생성
- `board/` 129개 절대URL → 루트상대 (`/board/...`)
- 모바일 38개 canonical 페이지별 정확
- 백업: `_bak_inherited_analytics_strip/`, `_bak_phase1_cleanup/`

## ✅ Phase 2 완료

도메인: **`sujainroicent.com`**

- ✅ 루트 PC 페이지의 `og:image` 절대URL → `https://sujainroicent.com/meta/thumb2.png` 일괄 교체
- ✅ `og:url`, canonical 등 사이트 전체 `sujain-roicent` 참조 정리 — 잔존 0개 (vr*.html의 `dasansub.cafe24.com/vr/2025/05.sujain-roicent/...`는 VR 벤더 경로라 정상)
- ✅ 신규 og:image 썸네일 생성 — `meta/thumb2.png` (확장자 .jpg 아닌 .png)
- ✅ `robots.txt` 생성 — `Allow: /`, `Disallow: /api/, /board/adm/, /board/data/, /_bak_`, sitemap 링크
- ✅ `sitemap.xml` 생성 — 32개 URL 등록 (메인 + 모든 sub 페이지)
- ✅ Naver Search Console verification meta 추가 (`7ecaea9de6a59839db9b90d993efb382dc19d29b`) — `index.htm` + `mobile/index.html`
- ✅ Google Search Console — **별도 meta 불필요**. GA4(`G-4BL7NCS5DG`) + GTM(`GTM-TDJXMMFD`) 기반으로 자동 소유권 인증 완료 (Search Console에서 확인)

## ✅ Phase 3 완료

라이브 페이지 응답에서 모두 확인됨:

- ✅ **GTM**: `GTM-TDJXMMFD`
- ✅ **GA4**: `G-4BL7NCS5DG`
- ✅ **Meta Pixel**: `1988984025053531` (init + PageView)
- ✅ **부정클릭시스템**: 보라웨어 상용 채택 — `protect_id=j764`, `script.boraware.kr/protect_script_v2.js` (커밋 `20a9580`)
- ✅ **자체 antifraud**: `/js/antifraud.js` body 끝 로드 (PC fullpage 충돌 회피로 head→body 이동, 커밋 `5dca535`)
- ✅ **Vercel `middleware.js`** 설치 — Supabase IP 차단 + 네이버 광고 클릭 GAS 서버사이드 기록 (`AKfycbwEENIblM0NCX7uQn-zVOY1IcwNj7aboQw98ZVWJ1dmrwDIs3S4QgF2Gv3smBhaIQxmqQ`)

## ⚠️ 잔여 미완료 항목

### 1. 카카오톡 채널 링크 (이전 분양사 채널 그대로)
- `index.htm:1729` — `https://kko.kakao.com/EgF4X3p1nK`
- `mobile/index.htm:581` — 동일
- **블로커**: 새 분양사 카카오 채널 URL 필요
- 참고: `mobile/index.html`(주력 모바일)은 메인 CONTACT 섹션이 관심고객등록 폼으로 교체되어(`bef21b8`) 카카오 링크 자체가 없음

### 2. (선택) Bing Webmaster Tools 인증
- `index.htm`/`mobile/index.html`에 `<!-- msvalidate.01 -->` 주석으로 자리만 있음
- 운영 안 하면 그대로 둬도 무방

### 3. (선택) Naver verification 적용 범위
- 현재 메인 2개 페이지에만 있음. 도메인 인증은 메인만 있어도 작동하므로 충분
- 모든 페이지 확장은 불필요

## 🔵 추가 권장 (지금 가능, 우선순위 낮음)

- 콘텐츠 검수 — 모든 페이지에서 이전 분양 정보(분양사명/모델하우스 주소/전화번호 1877-9896) 새 분양 정보로 교체
- 사이트 전체 용량 다이어트: `s/notosanskr/` 폰트(약 100MB+) — 사용 안 하면 제거 검토
- 이미지 webp 변환 (Vercel 자동 최적화 안 함, 수동 필요)

## 핵심 위치 매핑

| 자산 | 경로 |
|---|---|
| GitHub | `https://github.com/todaybds/sujainroicent` |
| Vercel | `https://sujainroicent.vercel.app` |
| 커스텀 도메인 | `https://sujainroicent.com` |
| 백업 폴더 | `_bak_*` (10+개, .gitignore에 제외됨) |
| 루트 PC 페이지 | `*.htm` / `*.html` (~60개) |
| 모바일 페이지 | `mobile/*.html` (~38개) |
| 게시판 (gnuboard 잔재) | `board/bbs/`, `board/adm/`, `board/js/`, `board/skin/` |
| 게시판 iframe 진입점 | `board/bbs/write.php.html`, `board/bbs/board.php.html`, `board/bbs/book_conf.php.html` |
| 메인 CSS (페이지마다) | `css/style-1.css` ~ `css/style-17.css` + 공통 `css/common-N.css` |
| device-redirect | `js/device-redirect.js` (paired 리스트 관리) |
| Edge 미들웨어 | `middleware.js` (Supabase IP 차단 + Naver 광고 GAS) |

## 다음 세션 시작 체크리스트

1. 새 분양사 카카오톡 채널 URL 받았는지 확인 → `index.htm` + `mobile/index.htm` 2곳 교체
2. (선택) Bing Webmaster Tools 운영 여부 결정
3. 콘텐츠 검수(이전 분양 정보 교체) — 분양사명/모델하우스 주소 등 사용자 확인 후 일괄 치환
