---
name: 프로젝트 개요 (수자인 로이센트 분양 사이트)
description: 인하대역 수자인 로이센트 사이트 전반 — 도메인, 분양 단계, 사이트 구조, 주요 페이지
type: project
---

# 인하대역 수자인 로이센트 (Sujain Roicent) 분양 사이트

## 도메인
- 운영 도메인: `sujain-roicent.co.kr` (canonical URL 기준)
- 로컬 개발: `127.0.0.1:3000` (정적 서버로 구동)

## 분양 단계
- **2026년 4월 현재**: GRAND OPEN 단계 (10/31 GRAND OPEN 표기)
- **청약 단계는 종료**: 청약안내(application*.html) 페이지 9개 삭제 완료 (2026-04-29)

## 사업 정보
- **시공**: BS한양 | 인천광역시 서구 청라한내로 110, 13층 4-비호
- **시행**: 아이월드주식회사 | 광주광역시 동구 서석로85번길 8-12
- **대표 전화**: 1877-9896 (이전: 032-875-0959 — 2026-04-29 변경 완료)
- **단지 위치**: 인천광역시 미추홀구 용현동 604-7번지 일원
- **세대수**: 1,199세대 (일반분양 959세대, 민간임대 240세대)

## 기술 스택
- **HTML**: 정적 파일, 빌드 시스템 없음
- **CSS**: 18개 style 파일 (style-1.css ~ style-17.css + style.css)
- **JS**: jQuery 3.6, Swiper 11, Slick, GSAP, FullPage.js (PC)
- **모바일 별도 라이브러리**: jQuery 3.7, Slick, ScrollMagic, GSAP

## 사이트 구조 요약
- **PC 버전**: 프로젝트 루트의 `*.html`/`*.htm` 파일들 (현재 51개)
- **모바일 버전**: `mobile/` 폴더 안의 동일 페이지들 (45개)
- **자동 분기**: `js/device-redirect.js`가 viewport ≤ 768px → 모바일, > 768px → PC

## 주요 페이지 카테고리
| 카테고리 | 페이지들 |
|---|---|
| 사업안내 | planning, brand, location, premium, contact |
| 단지안내 | complex, community, system |
| 상품안내 | unit (+ unit-1~3), vr (+ vr-1~3), interior, item_list, magam (+ magam-1~3) |
| 분양안내 | supply, schedule (메뉴 비활성) |
| 계약안내 | contract, document_capital, stampduty, notice02, document_common(+_01~05) |
| 홍보센터 | news, pr (+ pr2/pr3), event_open(+2~4), notice |
| 관심고객등록 | customer |
| 기타 | reservation01~03 (+ _check), magam, vr, unit |
