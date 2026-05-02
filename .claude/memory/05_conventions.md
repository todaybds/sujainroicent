---
name: 작업 컨벤션 (필수 패턴)
description: 이 프로젝트 작업 시 반드시 지켜야 할 패턴과 회피해야 할 함정
type: feedback
---

# 작업 컨벤션

## 필수: 수정 전 백업
**Why**: 프로젝트가 git 추적되지 않음 → 실수 시 복구 불가능

**How to apply**: 어떤 일괄 작업이든 다음 패턴 사용:
```bash
mkdir -p _bak_<작업명>
for f in <대상_파일들>; do
  cp "$f" "_bak_<작업명>/$(basename $f).bak"
done
# ... 변경 작업 ...
```

단일 파일은 `<원본>.before-<설명>.bak` 명명.

## 필수: 60+개 파일 일괄 수정 시 검증 단계 분리
**Why**: 한 파일에 잘못 적용된 패턴이 60개로 확산되면 복구 비용 큼

**How to apply**:
1. 1개 파일에 변경 적용 → 결과 검증
2. 검증 OK → 나머지 일괄 적용
3. 적용 후 `grep -l <패턴>` 으로 잔여 확인

## 필수: HTML 주석 안의 태그 처리
**Why**: 이 프로젝트는 `<!-- <ul ...> ... -->` 같은 비활성 마크업이 많음. 단순 regex로 depth 추적 시 어긋남

**How to apply**: HTML 구조 변경 작업은 무조건 Python depth-tracking + `skip_comment()` 패턴 사용. [_transform_smenu.py](../../_transform_smenu.py) 참고.

## 회피: non-greedy regex로 HTML 매칭
**Why**: `<li ...>...</li>` 같은 nested 구조에서 non-greedy `.*?`는 가장 가까운 close에 매칭됨 → 잘못된 페어 잡음

**How to apply**: 단순 치환은 sed로, 구조적 변경은 depth tracking 스크립트로.

## 필수: PC와 모바일 영향 범위 분리
**Why**: PC/모바일이 별개 마크업 + 별개 CSS → 한쪽만 수정해도 다른 쪽엔 영향 없음

**How to apply**: 사용자가 "모바일만" 또는 "PC만" 명시했을 때 반드시 그 범위만 수정. 헷갈리면 확인 질문.

## 필수: 17개 style 파일 동기화
**Why**: PC가 페이지마다 다른 style-N.css 사용 → 한 파일만 바꾸면 다른 페이지에서 깨짐

**How to apply**: PC CSS 룰 변경 시 `for f in css/style-{1..17}.css` 패턴 사용 (또는 적절한 범위).

## 권장: 캐시 새로고침 안내
**Why**: HTML/CSS/JS 변경 후 브라우저 캐시 때문에 변화 안 보일 수 있음 → 사용자 혼란

**How to apply**: 작업 보고서 마지막에 항상 `Ctrl + Shift + R` 강력 새로고침 안내 포함.

## 권장: 보고서 형식
**Why**: 대규모 일괄 작업의 결과를 사용자가 빠르게 검증할 수 있어야 함

**How to apply**:
- "변경 항목" 표 (영향 범위 + 결과)
- "확인 방법" 섹션 (구체적 페이지 + 어떻게 확인)
- "백업" 섹션 (복원 명령 포함)
- "잔여 검증" 섹션 (`grep -l` 결과 0이면 깨끗)

## 회피: 새로운 의존성 추가
**Why**: 기존 사이트는 정적 파일 그대로 운영 → npm/빌드 도구 도입 시 운영 비용 급증

**How to apply**: 외부 라이브러리 추가는 가능한 피하고, vanilla JS / 기존 라이브러리(jQuery, Swiper, Slick, GSAP)로 해결.

## 권장: 사용자 확인 후 파일 삭제
**Why**: 삭제는 일괄 수정보다 위험 부담 큼

**How to apply**: 파일 삭제는 항상 백업 후 + `rm -v`로 출력 + 결과 확인. 확실하지 않으면 묻기.

## 권장: 1개 표본 → 60개 일괄 패턴
**Why**: 사용자가 결과를 미리 볼 수 있어 안심 + 잘못된 방향 조기 발견

**How to apply**: 대규모 작업 전 "표본 1개 작업 → 사용자 확인 → 나머지 일괄" 흐름 제안.
