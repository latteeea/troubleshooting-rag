from generation import format_docs, generate
from graders import (
    grade_answer,
    grade_hallucination,
    grade_retrieval,
    rewrite_question,
)
from retriever import retrieve
from state import GraphState


def retrieve_node(state: GraphState) -> dict:
    print("==== [RETRIEVE] ====")
    question = state["question"]
    strategy = state.get("strategy", "markdown")
    documents = retrieve(query=question, strategy=strategy, k=4)
    return {"documents": documents}


def grade_documents_node(state: GraphState) -> dict:
    print("==== [GRADE DOCUMENTS] ====")
    question = state["original_question"]  # Day3-3: 판정·생성은 원 질문 기준
    documents = state["documents"]

    filtered_docs = []
    for doc in documents:
        score = grade_retrieval(question=question, document=doc.page_content)
        if score.binary_score == "yes":
            print("==== GRADE: DOCUMENT RELEVANT ====")
            filtered_docs.append(doc)
        else:
            print("==== GRADE: DOCUMENT NOT RELEVANT ====")

    return {"documents": filtered_docs}


MAX_REWRITE = 2
MAX_GENERATION = 3

NO_RECORD_ANSWER = "질문과 관련된 기록을 찾지 못했습니다. 다른 표현이나 키워드로 다시 물어봐 주세요."
UNVERIFIED_NOTE = "\n\n※ 이 답변의 일부 내용은 기록에서 근거를 확인하지 못했습니다."


def generate_node(state: GraphState) -> dict:
    print("==== [GENERATE] ====")
    question = state["original_question"]  # Day3-3: 판정·생성은 원 질문 기준
    documents = state["documents"]
    generation = generate(
        question,
        documents,
        tag="agentic_generate",
        feedback=state.get("hallucination_feedback", ""),
    )
    attempts = state.get("generation_attempts", 0) + 1
    return {"generation": generation, "generation_attempts": attempts}


def transform_query_node(state: GraphState) -> dict:
    print("==== [TRANSFORM QUERY] ====")
    # Day3-3: 재작성된 쿼리를 다시 재작성하면 원 질문에서 점점 멀어지므로 항상 원 질문에서 출발한다
    previous = state["question"] if state.get("rewrite_count", 0) > 0 else ""
    better_question = rewrite_question(state["original_question"], previous_query=previous)
    rewrite_count = state.get("rewrite_count", 0) + 1
    print(f"==== REWRITTEN: {better_question} ====")
    # 새 검색 결과에는 이전 피드백이 맞지 않으므로 비운다 (생성 횟수 상한은 전체 기준으로 유지)
    return {
        "question": better_question,
        "rewrite_count": rewrite_count,
        "hallucination_feedback": "",
    }


def no_record_node(state: GraphState) -> dict:
    """Day3-2: rewrite를 다 써도 관련 문서가 0개면 빈 context로 생성하지 않고 종료한다."""
    print("==== [NO RECORD] ====")
    return {"generation": NO_RECORD_ANSWER, "documents": []}


def flag_unverified_node(state: GraphState) -> dict:
    """Day3-2: 재생성 상한까지 근거 확인에 실패하면 검증 없이 통과시키지 않고, 미검증임을 표시한다."""
    print("==== [FLAG UNVERIFIED] ====")
    return {"generation": state["generation"] + UNVERIFIED_NOTE}


def decide_to_generate(state: GraphState) -> str:
    print("==== [ASSESS GRADED DOCUMENTS] ====")
    if state["documents"]:
        print("==== [DECISION: GENERATE] ====")
        return "generate"

    if state.get("rewrite_count", 0) >= MAX_REWRITE:
        print("==== [DECISION: NO RELEVANT DOCS AFTER MAX REWRITE, END] ====")
        return "no_record"

    print("==== [DECISION: NO RELEVANT DOCS, TRANSFORM QUERY] ====")
    return "transform_query"


def check_generation_node(state: GraphState) -> dict:
    """Day3-2: 환각·답변 검사를 노드로 옮겼다 (판정 이유를 state에 남겨 재생성에 쓰기 위해).

    이전 구조는 rewrite 2회 또는 생성 3회에 도달하면 검사 자체를 건너뛰었다.
    지금은 항상 검사하고, 상한 처리는 route_after_check에서 한다.
    """
    print("==== [CHECK HALLUCINATIONS] ====")
    question = state["original_question"]  # Day3-3: 판정·생성은 원 질문 기준
    generation = state["generation"]

    facts = format_docs(state["documents"])
    hallucination = grade_hallucination(documents=facts, generation=generation)
    if hallucination.binary_score != "yes":
        print("==== [GRADE: NOT GROUNDED] ====")
        return {
            "grounded": False,
            "answers_question": False,
            "hallucination_feedback": hallucination.reason or "근거가 확인되지 않은 주장이 있음",
        }

    print("==== [GRADE GENERATION vs QUESTION] ====")
    answer = grade_answer(question=question, generation=generation)
    return {
        "grounded": True,
        "answers_question": answer.binary_score == "yes",
        "hallucination_feedback": "",
    }


def route_after_check(state: GraphState) -> str:
    if not state["grounded"]:
        if state.get("generation_attempts", 0) < MAX_GENERATION:
            print("==== [DECISION: NOT GROUNDED, RE-GENERATE WITH FEEDBACK] ====")
            return "regenerate"
        print("==== [DECISION: NOT GROUNDED AT MAX ATTEMPTS, FLAG] ====")
        return "unverified"

    if state["answers_question"]:
        print("==== [DECISION: GROUNDED AND ANSWERS QUESTION] ====")
        return "accept"

    if state.get("rewrite_count", 0) < MAX_REWRITE:
        print("==== [DECISION: DOES NOT ANSWER QUESTION, TRANSFORM QUERY] ====")
        return "transform_query"

    # 근거는 있지만 질문에 충분히 답하지 못함 → 더 돌 수 없으니 근거 있는 답을 그대로 반환
    print("==== [DECISION: GROUNDED BUT PARTIAL AT MAX REWRITE, ACCEPT] ====")
    return "accept"
