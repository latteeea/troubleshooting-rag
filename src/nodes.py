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
    generation = generate(question, documents, tag="agentic_generate")
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
