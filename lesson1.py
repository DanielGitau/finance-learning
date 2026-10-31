# Lesson 1: variables, numbers and text
premium = 1000000  # gross written premium
claims = 620000  # incurred claims
expenses = 250000  # acquisition and admin costs

loss_ratio = claims / premium  # loss ratio
expense_ratio = expenses / premium  # expense ratio
combined_ratio = loss_ratio + expense_ratio  # combined ratio
underwriting_profit = premium - claims - expenses  # underwriting profit

print(f"Loss Ratio: {loss_ratio:.2%}")
print(f"Expense Ratio: {expense_ratio:.2%}")
print(f"Combined Ratio: {combined_ratio:.2%}")
print(f"Underwriting Profit: ${underwriting_profit:,}")

cession_rate = 0.30  # reinsurance cession rate in a QS Treaty
ceded_claims = claims * cession_rate  # claims ceded to reinsurer
ceded_premium = premium * cession_rate  # premium ceded to reinsurer

print(f"Ceded Claims: ${ceded_claims:,}")
print(f"Ceded Premium: ${ceded_premium:,}")