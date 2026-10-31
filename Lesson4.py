#Lesson 4: functons
def loss_ratio(premium, claims):
    """Calculate the loss ratio given premium and claims."""
    return claims / premium

def combined_ratio(claims, expenses, premium):
    """Calculate the combined ratio given claims, expenses, and premium."""
    return (claims + expenses) / premium

def quota_share(premium, claims, cession_rate):
    """Calculate the quota share given premium, claims, and cession rate."""
    ceded_premium = premium * cession_rate
    ceded_claims = claims * cession_rate
    return ceded_premium, ceded_claims

portfolio = {
    "property": {"premium": 500_000, "claims": 300_000, "expenses": 125_000},
    "Marine": {"premium": 300_000, "claims": 150_000, "expenses": 75_000},
    "D&O": {"premium": 200_000, "claims": 170_000, "expenses": 50_000},
    "Engineering": {"premium": 400_000, "claims": 220_000, "expenses": 110_000},
}

print(f"{'Class':<10} | {'LR':<10} | {'CR':<10}")
for name, data in portfolio.items():
    lr = loss_ratio(data["premium"], data["claims"])
    cr = combined_ratio(data["claims"], data["expenses"], data["premium"]) 
    print(f"{name:<10} | {lr:>8.1%} | {cr:>8.1%}")

ceded_premium, ceded_claims = quota_share(1_000_000, 620_000, 0.30)
print(f"\nCeded Premium: {ceded_premium:,.0f}")
print(f"Ceded Claims: {ceded_claims:,.0f}")

def expected_loss_ratio(pd, lgd, ead):
    return pd * lgd * ead

el = expected_loss_ratio(0.02, 0.6, 1_000_000)
print(f"\nExpected Loss: {el:,.0f}")