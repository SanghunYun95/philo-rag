# Contract Ledger BMAD-METHOD 통합 가이드라인

이 문서는 AI 협업 효율을 극대화하기 위해 BMAD-METHOD(Behavior-driven, Model-based Analysis and Design)를 `Contract Ledger` 프로젝트에 적용하는 전체 규칙과 활용법을 담고 있습니다.

---

## 1. 핵심 원칙 (Core Philosophy)

- **Docs-as-Code:** 모든 기능의 시작은 `documents/stories/` 내의 스토리 파일입니다.
- **Behavior-driven:** 기능은 사용자의 행동과 기대 결과(Acceptance Criteria) 중심으로 정의합니다.
- **Model-based:** 복잡한 로직은 텍스트보다는 구조화된 모델(Mermaid 다이어그램, JSON 스키마 등)로 표현합니다.
- **Context Integrity:** 문서를 스토리 단위로 쪼개어 AI가 필요한 정보에만 집중하게 합니다.

---

## 2. 단계별 페르소나 및 지침 (Persona & Guidelines)

### 📋 [Analysis Phase] - 비즈니스 분석가 (Analyst)

- **목표:** 모호한 요구사항을 명확한 '스토리(Story)'로 변환합니다.
- **결과물:** `documents/stories/ID.story_name.md` (Gherkin 스타일의 Behavior 정의 포함)
- **지침:** "사용자가 ~할 때, ~한 결과가 나와야 한다"는 비즈니스 로직에 집중합니다.

### 📐 [Architecture Phase] - 시스템 설계자 (Architect)

- **목표:** 스토리를 기술적으로 구현하기 위한 설계도를 그립니다.
- **결과물:** 스토리 파일 내 `Architecture Notes`, 다이어그램, API 스펙.
- **지침:** 데이터베이스 스키마, 인프라 제약, 보안 정책을 준수하는지 검증합니다.

### 💻 [Implementation Phase] - 시니어 개발자 (Developer)

- **목표:** 설계도를 바탕으로 무결점 코드를 작성합니다.
- **결과물:** 소스 코드 및 유닛 테스트.
- **지침:** 스토리의 `Acceptance Criteria`를 하나씩 체크하며 구현합니다.

### 🔍 [Review Phase] - QA 엔지니어 (QA/Review)

- **목표:** 코드와 스토리의 일치성을 검증하고 품질을 높입니다.
- **결과물:** 코드 리뷰 리포트, 테스트 결과.
- **지침:** "이 코드가 처음 기획한 행동(Behavior)과 일치하는가?"를 핵심 질문으로 던집니다.

---

## 3. 실무 활용 예시 (Usage Examples)

### ① 기획 및 설계 시나리오

**지시:** "BMAD 스킬로 'AI 기반 계약 생애주기 관리(CLM) 플랫폼을 위한 공통 시스템(Shared System) 백엔드 코어 모듈' 스토리 파일 만들어줘."
**AI 행동:** `documents/stories/001.clm-shared-system-core-module.md` 생성 후 승인 요청.

### ② 프롬프트 예시

- "BMAD 스킬 사용해서 기능을 만들고 싶은데 스토리 파일부터 작성해줄래?"
- "BMAD 스킬 사용해서 이제 설계자 모드로 이 스토리의 데이터 모델링을 해줘."
- "BMAD 스킬 사용해서 구현된 코드가 스토리의 Acceptance Criteria를 만족하는지 리뷰해줘."

---

## 4. 워크플로우 규칙 (Workflow)

1. 사용자가 기능을 요청하면 반드시 `Analysis` 단계로 시작하여 스토리 파일을 만듭니다.
2. 각 단계를 넘어갈 때마다 승인을 받습니다.
3. 코드 수정 시 관련된 스토리 파일도 함께 업데이트하여 항상 싱크를 맞춥니다.
