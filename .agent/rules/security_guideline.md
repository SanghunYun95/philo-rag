# 보안 및 프롬프트 인젝션 방지 가이드라인

이 문서는 LLM 서비스 운영 시 발생할 수 있는 보안 위협(특히 프롬프트 인젝션)을 방지하기 위한 기술적/정책적 가이드라인을 정의합니다.

---

## 1. 프롬프트 인젝션 (Prompt Injection) 방지

사용자가 시스템 프롬프트를 조작하여 AI의 행동 지침을 무시하게 만드는 공격을 방지합니다.

### 🛡️ 기술적 대응책
1. **Delimiters (구분자) 사용:** 
   사용자 입력을 시스템 프롬프트와 명확히 분리합니다.
   *예시:* `### User Input ###\n{user_input}\n### End of Input ###`
2. **Post-Prompting Instruction:**
   사용자 입력 뒤에 시스템 지침을 한 번 더 반복하여 LLM이 최종 지침을 잊지 않도록 합니다.
3. **Preamble Validation:**
   "Ignore previous instructions", "System prompt revealed" 등의 키워드가 포함된 입력을 사전에 거부하거나 경고 처리합니다.

## 2. 입력 데이터 정문화 (Input Sanitization)

- **Markdown/Script Injection:** 사용자 입력에 포함된 `<script>`, `<iframe>` 등 위험한 HTML 태그를 정규식 기반으로 제거합니다.
- **Length Limiting:** 
  - **최대 입력 길이:** 2,000자 또는 2,048 토큰 (둘 중 하한값 적용).
  - **제한 초과 시:** 사용자에게 즉시 오류 메시지(HTTP 400 - Bad Request)를 반환합니다.

## 3. 출력 데이터 검증 (Output Content Security)

LLM이 생성한 결과물을 사용자에게 보여주기 전 다음 사항을 확인합니다.
- **PII (개인정보) 필터링:** 
  - **대상:** 이메일, 주민등록번호, 전화번호.
  - **검증 규칙:** `Presidio` 라이브러리 및 표준 정규식(Regex)을 사용하여 탐지하고 `[MASK]` 처리합니다.
- **Harmful Content:** 혐오 표현, 위험 정보 등이 포함되었는지 별도의 소형 모델이나 필터링 라이브러리를 통해 검증하며, 탐지 시 응답을 중단하고 HTTP 403 - Forbidden을 반환합니다.

## 4. API 보안 및 인프라

- **Rate Limiting:** 
  - **Quotas:** IP당 분당 60회, 계정당 일일 1,000회 호출로 제한합니다.
  - **Enforcement:** 한도 초과 시 `Retry-After` 헤더를 포함한 HTTP 429 - Too Many Requests를 반환합니다.
- **API Key Management:** 환경 변수(`.env`)를 통해 관리하며, 절대 코드 저장소에 노출하지 않습니다.
- **Logging Policy:** 
  - 익명화된 인시던트 ID와 규칙 ID만 로깅하며, 원문 데이터(특히 PII)는 절대 로그에 남기지 않습니다.

---

> [!IMPORTANT]
> **보안은 지속적인 과정입니다.** 정기적으로 최신 LLM 공격 사례를 모니터링하고 가이드를 업데이트하세요.
