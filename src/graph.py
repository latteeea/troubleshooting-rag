from langgraph.graph import END, START, StateGraph

from nodes import (
    check_generation_node,
    decide_to_generate,
    flag_unverified_node,
    generate_node,
    grade_documents_node,
    no_record_node,
    retrieve_node,
    route_after_check,
    transform_query_node,
)
from state import GraphState


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_documents", grade_documents_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("check_generation", check_generation_node)
    workflow.add_node("transform_query", transform_query_node)
    workflow.add_node("no_record", no_record_node)
    workflow.add_node("flag_unverified", flag_unverified_node)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "generate": "generate",
            "transform_query": "transform_query",
            "no_record": "no_record",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_edge("generate", "check_generation")
    workflow.add_conditional_edges(
        "check_generation",
        route_after_check,
        {
            "accept": END,
            "regenerate": "generate",
            "unverified": "flag_unverified",
            "transform_query": "transform_query",
        },
    )
    workflow.add_edge("no_record", END)
    workflow.add_edge("flag_unverified", END)

    return workflow.compile()


def run_agentic_rag(
    question: str,
    strategy: str = "markdown",
) -> dict:
    app = build_graph()
    result = app.invoke(
        {
            "question": question,
            "original_question": question,
            "generation": "",
            "documents": [],
            "strategy": strategy,
            "rewrite_count": 0,
            "generation_attempts": 0,
            "hallucination_feedback": "",
            "grounded": False,
            "answers_question": False,
        }
    )

    sources = [
        {
            "source": doc.metadata.get("source"),
            "filename": doc.metadata.get("filename"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "strategy": doc.metadata.get("chunk_strategy"),
        }
        for doc in result.get("documents", [])
    ]

    return {
        "question": result.get("original_question", question),
        "rewritten_question": result.get("question", question),
        "rewrite_count": result.get("rewrite_count", 0),
        "strategy": strategy,
        "answer": result.get("generation", ""),
        "sources": sources,
    }
