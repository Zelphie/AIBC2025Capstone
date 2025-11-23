# backend/simulator.py

from backend.config import CURRENT_YEAR_BRS, CURRENT_YEAR_FRS, CURRENT_YEAR_ERS
from dataclasses import dataclass
from typing import List, Dict
import math

@dataclass
class RetirementInputs:
    current_age: int
    retirement_age: int
    current_savings: float  # total CPF savings for now
    monthly_contribution: float  # estimated amount going into retirement-related CPF
    salary_growth_rate: float  # e.g. 0.02 for 2% per year
    assumed_return_rate: float  # e.g. 0.035 for 3.5% per year


@dataclass
class ScenarioResult:
    name: str
    retirement_age: int
    projected_savings: float
    notes: str = ""


def project_savings(inputs: RetirementInputs) -> float:
    """
    Very simplified projection:
    - Contributions grow at salary_growth_rate per year.
    - Savings grow at assumed_return_rate per year.
    - Compounded annually.
    """
    years = inputs.retirement_age - inputs.current_age
    if years < 0:
        raise ValueError("Retirement age must be >= current age")

    balance = inputs.current_savings
    annual_contribution = inputs.monthly_contribution * 12

    for year in range(years):
        # Add this year's contribution
        balance += annual_contribution
        # Apply investment/interest growth
        balance *= (1 + inputs.assumed_return_rate)
        # Grow contributions for next year (salary growth)
        annual_contribution *= (1 + inputs.salary_growth_rate)

    return balance


def build_scenarios(inputs: RetirementInputs) -> List[ScenarioResult]:
    """
    Build a few simple comparison scenarios:
    - Base case
    - Retire 2 years later
    - Increase monthly contribution by 20%
    """
    scenarios: List[ScenarioResult] = []

    # 1) Base case
    base_projection = project_savings(inputs)
    scenarios.append(
        ScenarioResult(
            name="Base case",
            retirement_age=inputs.retirement_age,
            projected_savings=base_projection,
            notes="Projection using your current inputs."
        )
    )

    # 2) Retire 2 years later (if possible)
    if inputs.retirement_age + 2 <= 75:  # arbitrary cap
        later_inputs = RetirementInputs(
            current_age=inputs.current_age,
            retirement_age=inputs.retirement_age + 2,
            current_savings=inputs.current_savings,
            monthly_contribution=inputs.monthly_contribution,
            salary_growth_rate=inputs.salary_growth_rate,
            assumed_return_rate=inputs.assumed_return_rate,
        )
        later_projection = project_savings(later_inputs)
        scenarios.append(
            ScenarioResult(
                name="Retire 2 years later",
                retirement_age=later_inputs.retirement_age,
                projected_savings=later_projection,
                notes="Shows effect of delaying retirement by 2 years."
            )
        )

    # 3) Increase monthly contribution by 20%
    higher_contrib_inputs = RetirementInputs(
        current_age=inputs.current_age,
        retirement_age=inputs.retirement_age,
        current_savings=inputs.current_savings,
        monthly_contribution=inputs.monthly_contribution * 1.2,
        salary_growth_rate=inputs.salary_growth_rate,
        assumed_return_rate=inputs.assumed_return_rate,
    )
    higher_contrib_projection = project_savings(higher_contrib_inputs)
    scenarios.append(
        ScenarioResult(
            name="Increase contribution by 20%",
            retirement_age=higher_contrib_inputs.retirement_age,
            projected_savings=higher_contrib_projection,
            notes="Shows effect of increasing your monthly CPF contribution."
        )
    )

    return scenarios


def classify_vs_retirement_sums(
    projected_savings: float,
    brs: float,
    frs: float,
    ers: float,
) -> Dict[str, str]:
    """
    Classify where the projected savings sits relative to BRS/FRS/ERS.
    For now: simple text label and multiple of FRS.
    """
    multiple_of_frs = projected_savings / frs if frs > 0 else 0

    if projected_savings < brs:
        label = "Below BRS"
    elif brs <= projected_savings < frs:
        label = "Between BRS and FRS"
    elif frs <= projected_savings < ers:
        label = "Between FRS and ERS"
    else:
        label = "At or above ERS"

    return {
        "label": label,
        "multiple_of_frs": f"{multiple_of_frs:.2f} × FRS",
    }
