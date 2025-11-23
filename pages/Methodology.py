import streamlit as st

st.title("🧠 Methodology")

st.header("Overall Architecture")
st.image("https://i.imgur.com/aKXLOcV.png", caption="System architecture (LLM + RAG + Streamlit)")

st.markdown("### 💬 Use Case 1: Policy Explainer Flow (RAG)")
st.markdown(
"""
```mermaid
flowchart TD
    A[User asks a CPF question] --> B[Combine with profile inputs]
    B --> C[Embed question]
    C --> D[Vector retrieval (top-k chunks)]
    D --> E[LLM prompt with retrieved context]
    E --> F[LLM generates grounded answer]
    F --> G[Display answer + sources + disclaimers]
"""
)

st.markdown("### 🧮 Use Case 2: Retirement Simulator Flow (RAG + Projection)")
st.markdown(
"""
```mermaid
flowchart TD
    A[User enters age, savings, contributions] --> B[Run savings projection]
    B --> C[Classify result vs BRS/FRS/ERS]
    C --> D[Embed scenario summary]
    D --> E[Retrieve relevant policy chunks]
    E --> F[LLM produces explanation]
    F --> G[Show projections + chart + LLM explanation]
"""
)
