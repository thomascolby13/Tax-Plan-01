def individual_tax_2025_26(income: float) -> float:
    """Australian resident income tax + Medicare levy (simplified) for 2025-26 FY"""
    if income <= 0:
        return 0.0
    
    brackets = [
        (0,       18200,  0.00),
        (18201,   45000,  0.16),
        (45001,  135000,  0.30),
        (135001, 190000,  0.37),
        (190001, float('inf'), 0.45)
    ]
    
    tax = 0.0
    prev = 0
    
    for lower, upper, rate in brackets:
        if income <= prev:
            break
        taxable = min(income, upper) - max(prev, lower - 1 if lower > 0 else 0)
        if taxable > 0:
            tax += taxable * rate
        prev = upper
    
    # Simplified Medicare levy 2% (ignores low-income thresholds & surcharge)
    medicare = income * 0.02
    
    return round(tax + medicare, 2)


def company_tax_2025_26(income: float, rate: float = 0.25) -> float:
    """Company tax - default 25% for base rate entities"""
    return round(income * rate, 2)


def smsf_tax_accumulation_2025_26(income: float, rate: float = 0.15) -> float:
    """SMSF tax on taxable income/earnings in accumulation phase"""
    return round(income * rate, 2)


def tax_split_scenario(total_income: float,
                       individual_amount: float,
                       company_amount: float,
                       smsf_amount: float,
                       company_rate: float = 0.25) -> dict:
    """
    Calculate tax across individual, company (25%), and SMSF (15% accumulation)
    
    Checks that amounts add up to total_income (with small rounding tolerance)
    """
    allocated = individual_amount + company_amount + smsf_amount
    if abs(allocated - total_income) > 1.0:  # allow $1 tolerance for rounding
        raise ValueError(f"Amounts do not add up: {allocated:,.2f} != {total_income:,.2f}")
    
    ind_tax = individual_tax_2025_26(individual_amount)
    co_tax  = company_tax_2025_26(company_amount, company_rate)
    smsf_tax = smsf_tax_accumulation_2025_26(smsf_amount)
    
    total_tax = ind_tax + co_tax + smsf_tax
    
    return {
        'total_income': round(total_income, 2),
        'individual_income': round(individual_amount, 2),
        'individual_tax_incl_medicare': ind_tax,
        'company_income': round(company_amount, 2),
        'company_tax_25%': co_tax,
        'smsf_income_earnings': round(smsf_amount, 2),
        'smsf_tax_15%': smsf_tax,
        'total_tax_paid': round(total_tax, 2),
        'effective_overall_rate': round(total_tax / total_income * 100, 2) if total_income > 0 else 0.0,
        'tax_savings_vs_all_individual': round(individual_tax_2025_26(total_income) - total_tax, 2)
    }


def print_scenario(result: dict):
    print(f"{' Tax Split Scenario - 2025-26 FY ':=^70}")
    print(f"Total Income:                  ${result['total_income']:,.2f}")
    print("-" * 70)
    print(f"Individual portion:            ${result['individual_income']:,.2f}")
    print(f" → Tax + Medicare (est):      ${result['individual_tax_incl_medicare']:,.2f}")
    print(f"Company portion (25%):         ${result['company_income']:,.2f}")
    print(f" → Company tax:                ${result['company_tax_25%']:,.2f}")
    print(f"SMSF accumulation portion:     ${result['smsf_income_earnings']:,.2f}")
    print(f" → SMSF tax (15%):             ${result['smsf_tax_15%']:,.2f}")
    print("-" * 70)
    print(f"TOTAL TAX ACROSS ENTITIES:     ${result['total_tax_paid']:,.2f}")
    print(f"Effective overall rate:        {result['effective_overall_rate']}%")
    print(f"Compared to 100% individual:   SAVING ${result['tax_savings_vs_all_individual']:,.2f}")
    print("=" * 70)


# ────────────────────────────────────────────────
# Example usage - your scenario style
if __name__ == "__main__":
    # Example 1: Your suggested split style
    total = 200_000
    result = tax_split_scenario(
        total_income=total,
        individual_amount=60_000,
        company_amount=110_000,
        smsf_amount=30_000
    )
    print_scenario(result)
    
    print("\n")
    
    # Example 2: Larger total with different split
    total = 350_000
    result2 = tax_split_scenario(
        total_income=total,
        individual_amount=100_000,   # keep individual moderate to stay out of 45%
        company_amount=180_000,
        smsf_amount=70_000
    )
    print_scenario(result2)