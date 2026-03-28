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

- **Markdown/Script Injection:** 사용자 입력에 포함된 `<script>`, `<iframe>` 등 위험한 HTML 태그를 제거합니다.
- **Length Limiting:** 과도하게 긴 입력을 통한 서비스 거부(DoS) 공격을 방지하기 위해 입력 길이를 제한합니다.

## 3. 출력 데이터 검증 (Output Content Security)

LLM이 생성한 결과물을 사용자에게 보여주기 전 다음 사항을 확인합니다.
- **PII (개인정보) 필터링:** 주민등록번호, 이메일 주소 등이 노출되지 않도록 필터링합니다.
- **Harmful Content:** 혐오 표현, 위험 정보 등이 포함되었는지 별도의 소형 모델이나 필터링 라이브러리를 통해 검증합니다.

## 4. API 보안 및 인프라

- **Rate Limiting:** IP당/계정당 API 호출 횟수를 제한하여 무분별한 비용 발생 및 공격을 차단합니다.
- **API Key Management:** 환경 변수(`.env`)를 통해 관리하며, 절대 코드 저장소에 노출하지 않습니다.

---

> [!IMPORTANT]
> **보안은 지속적인 과정입니다.** 정기적으로 최신 LLM 공격 사례를 모니터링하고 가이드를 업데이트하세요.
