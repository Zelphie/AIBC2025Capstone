# backend/rag.py

from typing import List, Dict, Optional
from openai import OpenAI
from backend.vector_store import retrieve


from backend.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def _build_system_prompt() -> str:
    """
    System prompt used for both use cases.
    """
    return (
        "You are an assistant that explains CPF-related policies for educational purposes only. "
        "You must:\n"
        "- Use simple, neutral language.\n"
        "- Clearly state that your explanations are simplified.\n"
        "- Encourage users to refer to official CPF and gov.sg pages and calculators.\n"
        "- If you are unsure or lack information, say so explicitly.\n"
    )


def answer_policy_question(
    question: str,
    profile_context: Dict[str, str],
) -> str:
    """
    Use Case 1: Given a user question and profile context, run retrieval + LLM.
    """

    # Build a richer query for retrieval
    profile_bits = [
        f"{k}: {v}" for k, v in profile_context.items() if v and "Prefer not" not in v
    ]
    profile_str = "; ".join(profile_bits)

    retrieval_query = question
    if profile_str:
        retrieval_query += f" | profile: {profile_str}"

    # VERY simple heuristic: topic filter
    topic_filter = None
    if "withdraw" in question.lower() or "55" in question:
        topic_filter = "withdrawals"
    elif "brs" in question.lower() or "frs" in question.lower() or "ers" in question.lower():
        topic_filter = "retirement_sums"

    retrieved_chunks = retrieve(
        query=retrieval_query,
        k=5,
        topic_filter=topic_filter,
    )

    context_parts = []

    if profile_context:
        profile_text = "User profile:\n" + "\n".join(
            f"- {k}: {v}" for k, v in profile_context.items()
        )
        context_parts.append(profile_text)

    if retrieved_chunks:
        docs_text = "\n\n".join(
            f"[Source: {c.get('title','unknown')} - {c.get('source','')}] {c.get('text','')}"
            for c in retrieved_chunks
        )
        context_parts.append("Relevant policy excerpts:\n" + docs_text)
    else:
        context_parts.append(
            "No specific policy excerpts were retrieved. Answer based on general knowledge and be explicit about uncertainty."
        )

    full_context = "\n\n".join(context_parts)

    messages = [
        {"role": "system", "content": _build_system_prompt()},
        {
            "role": "user",
            "content": (
                f"{full_context}\n\n"
                f"User question:\n{question}\n\n"
                "Provide a clear explanation, list 3–5 key points, and end with a reminder "
                "to check official CPF sources and calculators."
            ),
        },
    ]

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
    )

    return response.choices[0].message.content


def explain_simulation_results(
    user_inputs: Dict,
    scenarios: List[Dict],
    base_classification: Dict[str, str],
) -> str:
    """
    Use Case 2: Explain the numeric results of the retirement simulator using RAG.
    """

    profile_text = "User simulation inputs:\n" + "\n".join(
        f"- {k}: {v}" for k, v in user_inputs.items()
    )

    scenarios_text_lines = []
    for s in scenarios:
        scenarios_text_lines.append(
            f"- {s['Scenario']}: retire at {s['Retirement age']} with projected savings "
            f"of S${s['Projected savings (S$)']:,.0f} ({s['Notes']})"
        )
    scenarios_text = "\n".join(scenarios_text_lines)

    classification_text = (
        f"Base scenario classification: {base_classification.get('label')} "
        f"({base_classification.get('multiple_of_frs')})."
    )

    # Build retrieval query
    retrieval_query = (
        f"retirement planning; projected savings classified as "
        f"{base_classification.get('label')} {base_classification.get('multiple_of_frs')}"
    )

    retrieved_chunks = retrieve(
        query=retrieval_query,
        k=5,
        topic_filter="retirement_sums",
    )

    context_parts = [profile_text, "Scenarios:\n" + scenarios_text, classification_text]

    if retrieved_chunks:
        docs_text = "\n\n".join(
            f"[Source: {c.get('title','unknown')} - {c.get('source','')}] {c.get('text','')}"
            for c in retrieved_chunks
        )
        context_parts.append("Relevant CPF information:\n" + docs_text)
    else:
        context_parts.append(
            "No specific CPF documents were retrieved. Explain in generic terms and be clear that this is illustrative."
        )

    full_context = "\n\n".join(context_parts)

    messages = [
        {"role": "system", "content": _build_system_prompt()},
        {
            "role": "user",
            "content": (
                f"{full_context}\n\n"
                "Explain what these projections mean in simple terms. "
                "Highlight:\n"
                "- Whether the user appears roughly below/around/above typical retirement benchmarks.\n"
                "- How delaying retirement or increasing contributions changes the picture.\n"
                "- 3–5 key insights or trade-offs.\n"
                "Be explicit that this is NOT an official CPF projection, and point the user to official calculators."
            ),
        },
    ]

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
    )

    return response.choices[0].message.content
