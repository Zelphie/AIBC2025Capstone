import streamlit as st
import pandas as pd

from backend.rag import answer_policy_question


st.title("💬 CPF Policy Explainer (Prototype)")

st.write(
    """
    Ask questions about CPF retirement policies in natural language.  
    This page uses a Large Language Model (LLM) for **educational** explanations only.
    Always verify with official CPF and gov.sg sources.
    """
)

# ============================
# ℹ️ BRS / FRS / ERS EXPLAINER (COLLAPSIBLE)
# ============================
with st.expander("ℹ️ What are BRS, FRS, and ERS? (click to expand)"):
    st.markdown(
        """
        CPF uses three benchmark amounts to determine how much you need for retirement:

        **• Basic Retirement Sum (BRS)**  
        The minimum level of retirement savings that provides a basic monthly payout.  
        Usually suitable for people who own a property **with sufficient lease** until age 95.

        **• Full Retirement Sum (FRS)**  
        Roughly **2 × BRS**.  
        Provides higher monthly payouts.  
        Members who do not own a property (or whose property doesn’t meet lease conditions) 
        typically need to set aside the FRS.

        **• Enhanced Retirement Sum (ERS)**  
        Roughly **3 × BRS**.  
        A voluntary higher savings level that provides the highest CPF LIFE payouts.

        These benchmarks help CPF estimate how much monthly income you may receive at retirement.  
        In this prototype, they are used only for **contextual explanations**, 
        not for official calculations.
        """
    )

    # --- Visual 1: Comparison table ---
    comparison_df = pd.DataFrame(
        [
            {
                "Retirement Sum": "BRS",
                "Relative level": "1 × (baseline)",
                "Typical use case": "Basic payout, usually for those with property (sufficient lease).",
            },
            {
                "Retirement Sum": "FRS",
                "Relative level": "2 × BRS",
                "Typical use case": "Higher payout; often needed if you don't have a qualifying property.",
            },
            {
                "Retirement Sum": "ERS",
                "Relative level": "3 × BRS",
                "Typical use case": "Optional higher savings for those who want higher CPF LIFE payouts.",
            },
        ]
    )

    st.markdown("**Quick comparison:**")
    st.table(comparison_df)

    # --- Visual 2: Simple bar chart for relative levels ---
    st.markdown("**Relative levels (not actual dollars):**")

    relative_df = pd.DataFrame(
        {
            "Retirement Sum": ["BRS", "FRS", "ERS"],
            "Relative amount": [1, 2, 3],
        }
    ).set_index("Retirement Sum")

    st.bar_chart(relative_df)

    st.caption(
        "Illustration only: FRS is roughly 2 × BRS, and ERS is roughly 3 × BRS. "
        "Exact dollar values change over time and depend on CPF's official schedules."
    )

    # --- Example: 35-year-old earning S$4,000/month ---
    st.markdown("### 👤 Example: 35-year-old earning S$4,000/month")

    st.markdown(
        """
        Imagine a typical **35-year-old Singaporean** with a monthly income of **S$4,000**.

        Over the next few decades, part of their CPF contributions will go into retirement savings.
        How might BRS, FRS and ERS matter to them?

        Below is a **story-style illustration** (not an official projection):
        """
    )

    example_df = pd.DataFrame(
        [
            {
                "If they aim for...": "BRS",
                "What it roughly means": (
                    "They are okay with a more basic level of monthly payout in retirement, "
                    "and they expect to still own a home with enough lease."
                ),
            },
            {
                "If they aim for...": "FRS",
                "What it roughly means": (
                    "They prefer a more comfortable payout, or they might not have a property "
                    "that qualifies them to use BRS. They are targeting about twice the baseline savings."
                ),
            },
            {
                "If they aim for...": "ERS",
                "What it roughly means": (
                    "They want the highest CPF LIFE payouts they can get through CPF, and are willing "
                    "to commit substantially more savings (about three times the baseline)."
                ),
            },
        ]
    )

    st.table(example_df)

    st.caption(
        "This example is just to make the idea concrete. "
        "It does **not** represent actual CPF requirements or advice for any specific person."
    )

st.divider()


with st.form("policy_explainer_form"):
    col1, col2 = st.columns(2)

    with col1:
        age_band = st.selectbox(
            "Age band (optional)",
            ["Prefer not to say", "Below 35", "35–44", "45–54", "55–64", "65 and above"],
            index=0,
        )
        housing_status = st.selectbox(
            "Housing situation (optional)",
            [
                "Prefer not to say",
                "No property",
                "Own HDB",
                "Own private property",
            ],
            index=0,
        )

    with col2:
        savings_band = st.selectbox(
            "Rough CPF savings band (optional)",
            [
                "Prefer not to say",
                "Below BRS",
                "Around BRS",
                "Between BRS and FRS",
                "Around FRS",
                "Between FRS and ERS",
                "At or above ERS",
            ],
            index=0,
        )

    question = st.text_area(
        "Your question about CPF",
        placeholder="Example: How much can I withdraw from my CPF at age 55?",
        height=120,
    )

    submitted = st.form_submit_button("Ask")

if submitted:
    if not question.strip():
        st.error("Please enter a question.")
        st.stop()

    profile_context = {
        "Age band": age_band,
        "Housing status": housing_status,
        "Savings band": savings_band,
    }

    with st.spinner("Thinking..."):
        answer = answer_policy_question(
            question=question,
            profile_context=profile_context,
        )

    st.subheader("🧾 Answer (educational only)")
    st.markdown(answer)

    st.info(
        """
        ⚠️ This explanation is generated by an LLM for **educational purposes only**.  
        Please verify details using official CPF and gov.sg websites and calculators.
        """
    )
