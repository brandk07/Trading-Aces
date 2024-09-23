import numpy_financial as npf

loan_amount = 5000  # The total amount of the loan
annual_interest_rate = 0.045  # 5% annual interest rate
loan_term_years = 12  # Loan term in years
payments_per_year = 12  # Monthly payments

# Calculate the periodic interest rate
periodic_interest_rate = annual_interest_rate / payments_per_year

# Calculate the total number of payments
total_payments = loan_term_years * payments_per_year

# Calculate the payment amount
payment = npf.pmt(periodic_interest_rate, total_payments, -loan_amount)

print(f"Monthly payment: ${payment:.2f}")
print(f"Total payment: ${payment * total_payments:.2f}")
print(f"Total interest: ${payment * total_payments - loan_amount:.2f}")
