# Lesson 2: Lists and Loops
years = [2021, 2022, 2023, 2024, 2025]  # list of years
premiums = [800_000, 900_000, 1_000_000, 1_100_000, 1_200_000]  # list of premiums for each year
claims = [480_000, 700_000, 620_000, 560_000, 900_000]  # list of claims for each year

print("Year | Premium | Claims | Loss Ratio")
for year, premium, claim in zip(years, premiums, claims):
    loss_ratio = claim / premium  # calculate loss ratio for each year
    print(f"{year} | {premium:,} | {claim:,} | {loss_ratio:.2%}")

    if loss_ratio > 0.70:
        print("  ^ above 70% loss ratio threshold")
        print("Consider reviewing underwriting practices or reinsurance arrangements.")

total_premium = sum(premiums)  # total premium over the years
total_claims = sum(claims)  # total claims over the years
overall_loss_ratio = total_claims / total_premium  # calculate overall loss ratio
print(f"\nOverall Loss Ratio: {overall_loss_ratio:.2%}")