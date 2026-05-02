---
name: 라이브 준비 진행 상태
description: GitHub 푸시 + Vercel 배포 + 새 도메인 라이브를 위한 단계별 진행 상태. 다음 세션에서 바로 이어가기 위한 체크포인트
type: project
---

# 라이브 준비 (2026-04-29 시점)

## 컨텍스트

이 사이트는 이전 분양사이트 코드(원래 `sujain-roicent.co.kr`)를 그대로 복사한 상태에서 개편 중. **새 분양사가 GitHub 푸시 → Vercel 배포 → 새 도메인(아직 미정)으로 라이브할 예정**. 이전 사이트의 트래킹/하드코딩 URL을 모두 정리해야 함.

참조 자료(바탕화면 형제 폴더):
- `cantaviledition.com/` — Vercel 라이브 사례 (vercel.json, middleware.js, robots.txt, sitemap.xml)
- `unjeong-ipark.com/` — 디자인 참조
- `부정클릭방지시스템/` — 자체 V20 시스템 (GAS + antifraud.js)
- `사이트_정리.txt` — 라이브된 사이트 6개 URL 목록

## ✅ Phase 1 완료 (2026-04-29)

[02_modifications_log.md](02_modifications_log.md) 섹션 27 참조

- 이전 사이트 트래킹 ID 4종 완전 제거 (GTM-TGHF9M29 / AW-17370728994 / G-TNYYRLMMV8 / gtag/ 폴더)
- `.gitignore` + `vercel.json` 신규 생성
- `board/` 129개 절대URL → 루트상대 (`/board/...`)
- 모바일 38개 canonical 페이지별 정확
- 백업: `_bak_inherited_analytics_strip/`, `_bak_phase1_cleanup/`

## 🟡 Phase 2 — 새 도메인 결정 후

**필요 정보**: 사용자가 구매할 새 도메인 (예: `sujain-inha.com`)

작업 항목:
- 루트 PC 페이지(44개)의 `og:image` 절대URL `https://sujain-roicent.co.kr/meta/thumb2.jpg` → 새 도메인
- `og:url`, JSON-LD 등 사이트 전체에 남은 `sujain-roicent` 참조 일괄 치환 (현재 약 31개 파일에 잔존)
- **신규 og:image 썸네일 생성** — `meta/thumb2.jpg` 파일 자체가 없어서 og 공유 이미 깨진 상태. 새 분양 비주얼로 만들어야 함
- `robots.txt` 생성 (cantaviledition 패턴 참조: `Allow: /`, `Disallow: /api/`, sitemap 링크)
- `sitemap.xml` 생성 — index.htm + 모든 sub 페이지 URL 등록
- 검색엔진 콘솔 인증 meta 자리 마련:
  - `<meta name="google-site-verification" content="">`
  - `<meta name="naver-site-verification" content="">`
  - `<meta name="msvalidate.01" content="">` (Bing)
- KakaoTalk 채널 링크 교체 — `index.htm`, `mobile/index.html`, `mobile/index.htm`의 `kko.kakao.com/EgF4X3p1nK`

## 🟡 Phase 3 — 새 트래킹 ID 받은 후

**필요 정보**:
1. **GTM 또는 GA4 ID** — 둘 중 어느 방식으로 갈지 결정
2. **Google Ads (선택)** — 전환추적 필요시
3. **Meta Pixel ID**
4. **Kakao Pixel ID** + Daum kp.js 사용 여부
5. **Naver Search Ad 계정** (wcslog 추적용)
6. **부정클릭시스템 선택**:
   - (A) 자체 V20 시스템 — `바탕화면/부정클릭방지시스템/` (GAS 서버 + antifraud.js, 무료, 운영 부담 큼)
   - (B) boraware 같은 상용 — cantaviledition.com에서 사용, `protect_id` 받아서 1줄 삽입
   - (C) 둘 다

작업 항목:
- 결정된 트래킹 코드 4-5종을 모든 페이지 head/body에 일괄 삽입 (perl)
- 폼 제출 conversion 이벤트 연결 (`board/js/common.js`의 `GA_event()` 함수 활용)
- Vercel `middleware.js` 설치 (선택) — IP 차단 + 네이버 광고 클릭 서버사이드 기록 (Supabase 또는 GAS)

## 🔵 추가 권장 (지금 가능, 우선순위 낮음)

- 콘텐츠 검수 — 모든 페이지에서 이전 분양 정보(분양사명/모델하우스 주소/전화번호 1877-9896) 새 분양 정보로 교체
- 사이트 전체 용량 다이어트: `s/notosanskr/` 폰트(약 100MB+) — 사용 안 하면 제거 검토
- 이미지 webp 변환 (Vercel 자동 최적화 안 함, 수동 필요)

## 핵심 위치 매핑

| 자산 | 경로 |
|---|---|
| 백업 폴더 | `_bak_*` (10+개, .gitignore에 제외됨) |
| 루트 PC 페이지 | `*.htm` / `*.html` (~60개) |
| 모바일 페이지 | `mobile/*.html` (~38개) |
| 게시판 (gnuboard 잔재) | `board/bbs/`, `board/adm/`, `board/js/`, `board/skin/` |
| 게시판 iframe 진입점 | `board/bbs/write.php.html`, `board/bbs/board.php.html`, `board/bbs/book_conf.php.html` |
| 메인 CSS (페이지마다) | `css/style-1.css` ~ `css/style-17.css` + 공통 `css/common-N.css` |
| device-redirect | `js/device-redirect.js` (paired 리스트 관리) |

## 다음 세션 시작 체크리스트

1. 사용자에게 새 도메인 결정됐는지 확인
2. 트래킹 ID 받았는지 확인 (Meta Pixel, Naver, Kakao 등)
3. 부정클릭시스템 자체/상용 결정 확인
4. 결정된 항목부터 진행 (Phase 2 / Phase 3 / 둘 다)
5. 결정 안 됐으면 콘텐츠 검수(이전 분양 정보 교체) 진행
