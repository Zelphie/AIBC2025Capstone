import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend.rag import explain_simulation_results
from backend.config import CURRENT_YEAR_BRS, CURRENT_YEAR_FRS, CURRENT_YEAR_ERS


from backend.simulator import (
    RetirementInputs,
    build_scenarios,
    classify_vs_retirement_sums,
)

# Placeholder: you will later read these from config or RAG
CURRENT_YEAR_BRS = 106_500.0  # example only, update to latest official numbers
CURRENT_YEAR_FRS = 213_000.0
CURRENT_YEAR_ERS = 426_000.0

st.title("🧮 Retirement Planning Simulator")

st.write(
    """
    This simulator provides a **simplified, illustrative** projection of your CPF 
    retirement savings based on your inputs.  
    It is **not** an official CPF calculator. For exact figures, please use 
    CPF's official tools.
    """
)

with st.form("retirement_sim_form"):
    col1, col2 = st.columns(2)

    with col1:
        current_age = st.number_input(
            "Current age",
            min_value=18,
            max_value=70,
            value=35,
            step=1,
        )
        retirement_age = st.number_input(
            "Planned retirement age",
            min_value=current_age + 1,
            max_value=75,
            value=65,
            step=1,
        )
        current_savings = st.number_input(
            "Current total CPF savings (S$)",
            min_value=0.0,
            value=50_000.0,
            step=1_000.0,
            format="%.2f",
        )

    with col2:
        monthly_contribution = st.number_input(
            "Estimated monthly CPF contribution towards retirement (S$)",
            min_value=0.0,
            value=1_000.0,
            step=50.0,
            format="%.2f",
            help="You can approximate this using your payslip or CPF contribution breakdown.",
        )
        salary_growth_rate_pct = st.slider(
            "Expected annual salary growth rate (%)",
            min_value=0.0,
            max_value=5.0,
            value=2.0,
            step=0.5,
        )
        return_rate_choice = st.radio(
            "Assumed effective annual return on CPF retirement savings",
            options=[
                "Conservative (3.0%)",
                "Typical CPF-style (3.5%)",
                "Optimistic (4.0%)",
            ],
            index=1,
        )

    submitted = st.form_submit_button("Run simulation")

if submitted:
    # Map choice to numeric rate
    if "3.0" in return_rate_choice:
        assumed_return_rate = 0.03
    elif "3.5" in return_rate_choice:
        assumed_return_rate = 0.035
    else:
        assumed_return_rate = 0.04

    inputs = RetirementInputs(
        current_age=int(current_age),
        retirement_age=int(retirement_age),
        current_savings=float(current_savings),
        monthly_contribution=float(monthly_contribution),
        salary_growth_rate=salary_growth_rate_pct / 100.0,
        assumed_return_rate=assumed_return_rate,
    )

    try:
        scenarios = build_scenarios(inputs)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # Build DataFrame for display
    df = pd.DataFrame(
        [
            {
                "Scenario": s.name,
                "Retirement age": s.retirement_age,
                "Projected savings (S$)": round(s.projected_savings, 2),
                "Notes": s.notes,
            }
            for s in scenarios
        ]
    )

    st.subheader("📊 Scenario comparison")
    st.dataframe(df, use_container_width=True)

    # Classification vs BRS/FRS/ERS for base scenario
    base = scenarios[0]
    classification = classify_vs_retirement_sums(
        base.projected_savings,
        CURRENT_YEAR_BRS,
        CURRENT_YEAR_FRS,
        CURRENT_YEAR_ERS,
    )

    st.subheader("🎯 Interpretation (simplified)")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown(
            f"""
            **Base case – retire at age {base.retirement_age}:**

            - Projected savings: **S${base.projected_savings:,.0f}**  
            - Classification: **{classification['label']}**  
            - Relative to FRS: **{classification['multiple_of_frs']}**
            """
        )

    with col_right:
        st.markdown("**Reference (current year, for illustration):**")
        st.write(f"- BRS: S${CURRENT_YEAR_BRS:,.0f}")
        st.write(f"- FRS: S${CURRENT_YEAR_FRS:,.0f}")
        st.write(f"- ERS: S${CURRENT_YEAR_ERS:,.0f}")

    # Simple bar chart of scenarios
    st.subheader("📈 Visual comparison")

    fig, ax = plt.subplots()
    ax.bar(
        df["Scenario"],
        df["Projected savings (S$)"],
    )
    ax.set_ylabel("Projected savings (S$)")
    ax.set_xlabel("Scenario")
    ax.tick_params(axis="x", rotation=15)
    st.pyplot(fig)

    st.info(
        """
        ⚠️ **Disclaimer:** This is an educational illustration.  
        Actual CPF balances and payouts depend on your CPF account composition, 
        future policies, actual interest rates, and CPF LIFE plan. 
        Please refer to CPF’s official calculators for precise estimates.
        """
    )

    # --- LLM-driven explanation section ---
    st.subheader("🧠 Explanation (LLM-generated, educational only)")

    user_inputs_dict = {
        "current_age": current_age,
        "retirement_age": retirement_age,
        "current_savings": current_savings,
        "monthly_contribution": monthly_contribution,
        "salary_growth_rate_pct": salary_growth_rate_pct,
        "assumed_return_rate": assumed_return_rate,
    }

    scenarios_dicts = df.to_dict(orient="records")

    with st.spinner("Generating explanation..."):
        explanation = explain_simulation_results(
            user_inputs=user_inputs_dict,
            scenarios=scenarios_dicts,
            base_classification=classification,
        )

    st.markdown(explanation)

    st.info(
        """
        ⚠️ This explanation is generated by an LLM based on a **simplified simulator**.  
        It does **not** reflect your actual CPF balances or entitlements. 
        Always rely on official CPF calculators and statements for decisions.
        """
    )
