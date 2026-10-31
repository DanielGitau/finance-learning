# Lesson 3: dictionaries
portfolio = {
    "property": {"premium": 500_000, "claims": 300_000},
    "Marine": {"premium": 300_000, "claims": 150_000},
    "D&O": {"premium": 200_000, "claims": 170_000},
    "Engineering": {"premium": 400_000, "claims": 220_000},
}

print(f"{'Class':<10} | {'Premium':<10} | {'Claims':<10} | {'LR':<8}")

total_premium = 0
total_claims = 0

for name, data in portfolio.items():
    lr = data["claims"] / data["premium"]
    print(f"{name:<10} | {data['premium']:>10,} | {data['claims']:>10,} | {lr:>8.1%}")

    total_premium += data["premium"]
    total_claims += data["claims"]
    print(f"{'Total':<10} | {total_premium:>10,} | {total_claims:>10,} | {total_claims/total_premium:>8.1%}")