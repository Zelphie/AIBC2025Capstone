import streamlit as st
import pandas as pd

from backend.config import (
    CURRENT_YEAR_BRS,
    CURRENT_YEAR_FRS,
    CURRENT_YEAR_ERS,
    CURRENT_YEAR_LABEL,
)
from backend.rag import explain_simulation_results

# NOTE: Do NOT call st.set_page_config here; it's already called in Home.py.

st.title("🧮 CPF Retirement Planning Simulator")

st.markdown(
    """
This tool lets you run a **simplified projection** of your CPF retirement savings, 
based on a few basic assumptions.

You can explore:

- How your savings might grow until a chosen retirement age  
- How your projected balance compares to **BRS / FRS / ERS**  
- A narrative explanation of what the numbers might mean  

All results are **illustrative only** and do *not* reflect your actual CPF balances.
"""
)

st.markdown(
    f"""
**Reference (for context only, not exact):**  
- Basic Retirement Sum (BRS) for cohort year {CURRENT_YEAR_LABEL}: ~S${CURRENT_YEAR_BRS:,.0f}  
- Full Retirement Sum (FRS) for cohort year {CURRENT_YEAR_LABEL}: ~S${CURRENT_YEAR_FRS:,.0f}  
- Enhanced Retirement Sum (ERS) for cohort year {CURRENT_YEAR_LABEL}: ~S${CURRENT_YEAR_ERS:,.0f}  
"""
)

st.markdown("---")

# ---------------------------------------------------------------------
# Helpers: projection + classification
# ---------------------------------------------------------------------


def run_projection(
    current_age: int,
    retirement_age: int,
    current_savings: float,
    monthly_contribution: float,
    salary_growth_rate_pct: float,
    assumed_return_rate_pct: float,
) -> pd.DataFrame:
    years = list(range(current_age, retirement_age + 1))
    balance = current_savings
    monthly_contrib = monthly_contribution

    records = []

    growth_rate = salary_growth_rate_pct / 100.0
    return_rate = assumed_return_rate_pct / 100.0

    for age in years:
        records.append(
            {
                "Age": age,
                "Year": age - current_age,  # years from now
                "Projected savings (S$)": balance,
            }
        )
        # end of year: apply interest + contributions
        annual_contrib = monthly_contrib * 12.0
        balance = balance * (1.0 + return_rate) + annual_contrib
        monthly_contrib *= 1.0 + growth_rate

    df = pd.DataFrame(records)
    return df


def classify_against_frs(final_amount: float) -> dict:
    ratio = final_amount / CURRENT_YEAR_FRS if CURRENT_YEAR_FRS > 0 else 0.0

    if ratio < 0.8:
        label = "Below FRS"
    elif 0.8 <= ratio <= 1.2:
        label = "Around FRS"
    elif 1.2 < ratio <= 1.8:
        label = "Between FRS and ERS"
    else:
        label = "At or above ERS (approx.)"

    return {
        "label": label,
        "multiple_of_frs": f"≈ {ratio:0.2f} × FRS" if CURRENT_YEAR_FRS > 0 else "N/A",
    }


# ---------------------------------------------------------------------
# Initialise session_state for simulation
# ---------------------------------------------------------------------

if "simulation_ready" not in st.session_state:
    st.session_state.simulation_ready = False
    st.session_state.projection_df = None
    st.session_state.classification = None
    st.session_state.sim_inputs = None

# Defaults for inputs (used for presets)
default_values = {
    "current_age": 35,
    "retirement_age": 65,
    "current_savings": 50_000.0,
    "monthly_contribution": 800.0,
    "salary_growth_rate_pct": 2.0,
    "assumed_return_rate_pct": 4.0,
    "target_income": 2000.0,
}

for k, v in default_values.items():
    st.session_state.setdefault(k, v)

st.session_state.setdefault("last_preset", "Custom inputs")


def apply_preset(preset_name: str):
    """
    Set session_state values for inputs based on chosen preset.
    """
    if preset_name == "Typical 35-year-old (mid-income)":
        st.session_state.current_age = 35
        st.session_state.retirement_age = 65
        st.session_state.current_savings = 60_000.0
        st.session_state.monthly_contribution = 900.0
        st.session_state.salary_growth_rate_pct = 2.0
        st.session_state.assumed_return_rate_pct = 4.0
        st.session_state.target_income = 2200.0

    elif preset_name == "Age 45, catching up":
        st.session_state.current_age = 45
        st.session_state.retirement_age = 65
        st.session_state.current_savings = 140_000.0
        st.session_state.monthly_contribution = 1_000.0
        st.session_state.salary_growth_rate_pct = 1.5
        st.session_state.assumed_return_rate_pct = 4.0
        st.session_state.target_income = 2500.0

    elif preset_name == "Near retirement (age 55)":
        st.session_state.current_age = 55
        st.session_state.retirement_age = 65
        st.session_state.current_savings = 260_000.0
        st.session_state.monthly_contribution = 1_100.0
        st.session_state.salary_growth_rate_pct = 1.0
        st.session_state.assumed_return_rate_pct = 4.0
        st.session_state.target_income = 2500.0

    # Custom inputs: do nothing (keep whatever is in session_state)


# ---------------------------------------------------------------------
# Layout: Inputs + Results in tabs
# ---------------------------------------------------------------------

tab_inputs, tab_results = st.tabs(["🧮 Simulation inputs", "📊 Results & explanation"])

with tab_inputs:
    st.subheader("Enter your details (all values are approximate)")

    preset_options = [
        "Custom inputs",
        "Typical 35-year-old (mid-income)",
        "Age 45, catching up",
        "Near retirement (age 55)",
    ]

    preset = st.selectbox(
        "Quick presets (optional)",
        options=preset_options,
        index=preset_options.index(st.session_state.last_preset),
        help="Select a scenario to pre-fill the form, or choose 'Custom inputs' to set your own values.",
    )

    if preset != st.session_state.last_preset:
        st.session_state.last_preset = preset
        apply_preset(preset)
        st.experimental_rerun()

    with st.form("retirement_sim_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_age = st.slider(
                "Current age",
                min_value=21,
                max_value=65,
                key="current_age",
            )
            retirement_age = st.slider(
                "Planned retirement age",
                min_value=50,
                max_value=70,
                key="retirement_age",
            )
            current_savings = st.number_input(
                "Current CPF savings (S$)",
                min_value=0.0,
                step=1000.0,
                key="current_savings",
            )

        with col2:
            monthly_contribution = st.number_input(
                "Current monthly CPF contribution (S$)",
                min_value=0.0,
                step=50.0,
                key="monthly_contribution",
            )
            salary_growth_rate_pct = st.slider(
                "Expected annual growth in contributions",
                min_value=0.0,
                max_value=5.0,
                step=0.5,
                key="salary_growth_rate_pct",
                help="This is a simplified assumption and does not reflect official CPF projections.",
            )
            assumed_return_rate_pct = st.slider(
                "Assumed annual CPF return rate",
                min_value=2.0,
                max_value=5.0,
                step=0.5,
                key="assumed_return_rate_pct",
                help="Illustrative blended rate, not an official OA/SA/MA breakdown.",
            )

        target_income = st.number_input(
            "Target retirement income per month (S$, optional)",
            min_value=0.0,
            step=100.0,
            key="target_income",
        )

        submitted = st.form_submit_button("Run simulation")

    if submitted:
        if retirement_age <= current_age:
            st.error("Planned retirement age must be **greater than** current age.")
        else:
            with st.spinner("Running projection..."):
                df = run_projection(
                    current_age=current_age,
                    retirement_age=retirement_age,
                    current_savings=current_savings,
                    monthly_contribution=monthly_contribution,
                    salary_growth_rate_pct=salary_growth_rate_pct,
                    assumed_return_rate_pct=assumed_return_rate_pct,
                )

            final_amount = float(df["Projected savings (S$)"].iloc[-1])
            classification = classify_against_frs(final_amount)

            st.session_state.simulation_ready = True
            st.session_state.projection_df = df
            st.session_state.classification = classification
            st.session_state.sim_inputs = {
                "current_age": current_age,
                "retirement_age": retirement_age,
                "current_savings": current_savings,
                "monthly_contribution": monthly_contribution,
                "salary_growth_rate_pct": salary_growth_rate_pct,
                "assumed_return_rate_pct": assumed_return_rate_pct,
                "target_retirement_income": target_income,
            }

            st.success(
                "🎉 Your simulation is ready! Click on the **📊 Results & explanation** tab to view it."
            )
            st.info(
                "You can adjust your inputs and re-run the simulation at any time. "
                "The latest results will always appear in the Results tab."
            )

    # Show last simulation summary (if available)
    if st.session_state.simulation_ready and st.session_state.projection_df is not None:
        df_last = st.session_state.projection_df
        final_amount_last = float(df_last["Projected savings (S$)"].iloc[-1])
        classification_last = st.session_state.classification
        inputs_last = st.session_state.sim_inputs

        st.markdown("### 📌 Last simulation summary")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Retirement age", f"{inputs_last['retirement_age']} years")
        col_b.metric("Projected CPF savings", f"S${final_amount_last:,.0f}")
        col_c.metric("Relative to FRS", classification_last["multiple_of_frs"])
        st.caption("This summary reflects the most recent simulation you ran.")


with tab_results:
    if not st.session_state.get("simulation_ready", False):
        st.info("Run a simulation in the **🧮 Simulation inputs** tab to see results here.")
        st.stop()

    df = st.session_state.projection_df
    classification = st.session_state.classification
    sim_inputs = st.session_state.sim_inputs

    final_amount = float(df["Projected savings (S$)"].iloc[-1])
    retirement_age = sim_inputs["retirement_age"]
    target_income = sim_inputs["target_retirement_income"]

    st.subheader("📌 Scenario summary")
    col_a, col_b, col_c = st.columns(3)

    col_a.metric("Retirement age", f"{retirement_age} years")
    col_b.metric("Projected CPF savings", f"S${final_amount:,.0f}")
    col_c.metric("Relative to FRS", classification["multiple_of_frs"])

    st.caption(
        "Classification is approximate and uses the current FRS as a benchmark for illustration."
    )

    st.markdown("### 📈 Savings over time")
    st.line_chart(df.set_index("Age")["Projected savings (S$)"])

    st.markdown("### 📋 Detailed table")
    st.dataframe(
        df.style.format({"Projected savings (S$)": "S${:,.0f}"}),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("🧠 Explanation (AI-generated)")

    scenarios_dicts = [
        {
            "Scenario": "Base scenario",
            "Retirement age": retirement_age,
            "Projected savings (S$)": final_amount,
            "Notes": classification["label"],
        }
    ]

    with st.spinner("Generating explanation..."):
        explanation = explain_simulation_results(
            user_inputs=sim_inputs,
            scenarios=scenarios_dicts,
            base_classification=classification,
        )

    st.markdown(explanation)

    with st.expander("ℹ️ How to interpret these results", expanded=False):
        st.markdown(
            """
- This simulator uses **simplified assumptions** about interest and contributions.  
- Actual CPF balances depend on OA/SA/MA split, policy changes, and your exact history.  
- Use this as a **thinking tool**, not a source of truth.  
- Always check your real balances and use official CPF calculators for decisions.
"""
        )

    st.info(
        """
**Important:**  
This simulation and explanation are for **educational purposes only**.  
They do **not** represent actual CPF calculations or personalised financial advice.
"""
    )
