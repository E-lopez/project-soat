from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

def calculate_remaining_balance(
    scheduled_principal: Decimal,
    allocated_principal: Decimal
) -> Decimal:
    return scheduled_principal - allocated_principal

def calculate_remaining_interest(
    scheduled_interest: Decimal,
    allocated_interest: Decimal
) -> Decimal:
    return scheduled_interest - allocated_interest

def calculate_remaining_fees(
    scheduled_fees: Decimal,
    allocated_fees: Decimal
) -> Decimal:
    return scheduled_fees - allocated_fees

def calculate_total_balance(
    remaining_principal: Decimal,
    remaining_interest: Decimal,
    remaining_fees: Decimal
) -> Decimal:
    return remaining_principal + remaining_interest + remaining_fees

def get_monthly_rate(annual_rate: Decimal) -> Decimal:
    return annual_rate / Decimal('12')

def get_fee_amount(principal: Decimal) -> Decimal:
    taxes = principal * 4 / Decimal('1000')
    partial = (principal * Decimal('0.05') + taxes).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return max(partial.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), 100000)  # Minimum fee of 100,000
