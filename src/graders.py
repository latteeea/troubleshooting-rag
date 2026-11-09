"""Self-RAG grader / rewriter.

프롬프트 원문은 week4 그대로 유지한다 (Day1: 구조/프로바이더만 교체, 로직 변경 없음).
"""

from llm import complete, structured
from schemas import GradeAnswer, GradeDocuments, GradeHallucination

RETRIEVAL_GRADER_PROMPT = """너는 트러블슈팅 기록 RAG의 retrieval grader다.
검색된 문서가 사용자 질문과 관련 있는지 평가한다.

평가 기준:
- 키워드 또는 의미가 질문과 연결되면 relevant
- 증상·원인·해결·인과 관계 중 하나라도 질문에 도움이 되면 relevant
- 엄격할 필요 없음. 명백히 무관한 문서만 걸러낸다.

'yes' 또는 'no'로만 답한다."""

HALLUCINATION_GRADER_PROMPT = """너는 hallucination checker다.
생성된 답변이 제공된 문서(사실)에 근거하는지 평가한다.

- 문서에 없는 인과·사실을 단정하면 'no'
- 문서 내용을 요약·재구성한 것이면 'yes'
- [추측] 표시 없이 추측을 사실처럼 쓰면 'no'

binary_score는 'yes' 또는 'no'로 답한다.
'no'라면 reason에 문서에 근거가 없는 주장을 구체적으로 적는다 (재생성 시 그대로 전달된다)."""

ANSWER_GRADER_PROMPT = """너는 answer grader다.
생성된 답변이 사용자 질문을 실제로 해결하는지 평가한다.

- 인과 관계(A→B→C)를 묻는 질문이면 체인이 이어지는지 확인
- 원인·해결·인사이트를 구분했는지 확인
- 질문 핵심을 빠뜨렸으면 'no'
- 단, 답변이 "제공된 기록에 질문한 내용이 없다"고 명확히 밝히고 다른 내용을 질문의 답처럼 지어내지 않았다면 'yes'
  (근거 없는 답보다 정직한 기권이 낫다. 기권 자체를 '질문 핵심을 빠뜨림'으로 보지 않는다)

'yes' 또는 'no'로만 답한다."""

QUESTION_REWRITER_PROMPT = """너는 트러블슈팅 기록용 query rewriter다.
사용자의 자연어 질문을 벡터 검색에 맞는 검색 쿼리로 바꾼다.

규칙:
- 감정적·비유적·모호한 표현을 일반적인 기술 표현으로 바꾼다
  예: "다크 모드에서 글씨가 안 보이던 거" → "다크 모드 텍스트 색상 대비 테마 설정 문제"
- 질문에 없는 고유명사, 제품명, 설정 키, 에러 코드를 새로 만들어 넣지 않는다
  (기록에 없는 용어를 덧붙이면 엉뚱한 문서를 끌어온다)
- 증상, 원인, 해결 중 질문이 묻는 측면을 드러내는 일반 키워드를 포함한다
- 한 문장으로, 80자 이내로 출력한다
- 설명 없이 재작성된 쿼리만 반환한다"""


def grade_retrieval(question: str, document: str) -> GradeDocuments:
    user = f"Retrieved document:\n\n{document}\n\nUser question: {question}"
    return structured(RETRIEVAL_GRADER_PROMPT, user, GradeDocuments, tag="retrieval_grader")


def grade_hallucination(documents: str, generation: str) -> GradeHallucination:
    user = f"Set of facts:\n\n{documents}\n\nLLM generation: {generation}"
    # Day3-3: effort low → medium. low에서는 맞는 답도 반복 불합격(2단계 미검증 19%)해서 피드백 재생성이 내용을 깎아냈다.
    return structured(
        HALLUCINATION_GRADER_PROMPT, user, GradeHallucination, effort="medium", tag="hallucination_grader"
    )


def grade_answer(question: str, generation: str) -> GradeAnswer:
    user = f"User question:\n\n{question}\n\nLLM generation: {generation}"
    return structured(ANSWER_GRADER_PROMPT, user, GradeAnswer, tag="answer_grader")


def rewrite_question(question: str, previous_query: str = "") -> str:
    user = f"Initial question:\n\n{question}"
    if previous_query:
        user += f"\n\n이전에 시도한 검색 쿼리 (관련 기록을 찾지 못함): {previous_query}\n이와 다른 표현으로 작성한다."
    user += "\n\nImproved search query:"
    return complete(QUESTION_REWRITER_PROMPT, user, effort="low", tag="question_rewriter")
