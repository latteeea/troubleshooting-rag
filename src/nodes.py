from baseline import format_docs
from graders import (
    grade_answer,
    grade_hallucination,
    grade_retrieval,
    rewrite_question,
)
from llm import complete
from retriever import retrieve
from state import GraphState

GENERATION_PROMPT = """너는 사용자의 기술 트러블슈팅 기록을 기반으로 답변하는 Agentic RAG assistant다.

규칙:
- 제공된 context만 근거로 답한다. 문서에 없는 내용은 추측하지 않는다.
- 인과 관계 질문이면 A→B→C→D 형태로 시간·원인 순서를 복원한다.
- 답변 구조: 문제 상황 / 조사·원인 / 해결 / 인사이트
- 마지막에 참고 문서 source를 반드시 포함한다."""


def retrieve_node(state: GraphState) -> dict:
    print("==== [RETRIEVE] ====")
    question = state["question"]
    strategy = state.get("strategy", "markdown")
    documents = retrieve(query=question, strategy=strategy, k=4)
    return {"documents": documents}


def grade_documents_node(state: GraphState) -> dict:
    print("==== [GRADE DOCUMENTS] ====")
    question = state["question"]
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


def generate_node(state: GraphState) -> dict:
    print("==== [GENERATE] ====")
    question = state["question"]
    documents = state["documents"]
    context = format_docs(documents)

    user = f"질문: {question}\n\n검색된 context:\n{context}"
    generation = complete(GENERATION_PROMPT, user, tag="agentic_generate")
    attempts = state.get("generation_attempts", 0) + 1
    return {"generation": generation, "generation_attempts": attempts}


def transform_query_node(state: GraphState) -> dict:
    print("==== [TRANSFORM QUERY] ====")
    question = state["question"]
    better_question = rewrite_question(question)
    rewrite_count = state.get("rewrite_count", 0) + 1
    print(f"==== REWRITTEN: {better_question} ====")
    return {"question": better_question, "rewrite_count": rewrite_count}


def decide_to_generate(state: GraphState) -> str:
    print("==== [ASSESS GRADED DOCUMENTS] ====")
    filtered_documents = state["documents"]
    rewrite_count = state.get("rewrite_count", 0)

    if rewrite_count >= 2:
        print("==== [DECISION: MAX REWRITE REACHED, GENERATE ANYWAY] ====")
        return "generate"

    if not filtered_documents:
        print("==== [DECISION: NO RELEVANT DOCS, TRANSFORM QUERY] ====")
        return "transform_query"

    print("==== [DECISION: GENERATE] ====")
    return "generate"


def grade_generation(state: GraphState) -> str:
    print("==== [CHECK HALLUCINATIONS] ====")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    rewrite_count = state.get("rewrite_count", 0)
    generation_attempts = state.get("generation_attempts", 0)

    if rewrite_count >= 2 or generation_attempts >= 3:
        print("==== [DECISION: MAX RETRY REACHED, END] ====")
        return "relevant"

    facts = format_docs(documents)
    score = grade_hallucination(documents=facts, generation=generation)

    if score.binary_score != "yes":
        print("==== [DECISION: HALLUCINATION, RE-GENERATE] ====")
        return "hallucination"

    print("==== [GRADE GENERATION vs QUESTION] ====")
    score = grade_answer(question=question, generation=generation)

    if score.binary_score == "yes":
        print("==== [DECISION: GENERATION ADDRESSES QUESTION] ====")
        return "relevant"

    print("==== [DECISION: GENERATION DOES NOT ADDRESS QUESTION] ====")
    return "not relevant"
