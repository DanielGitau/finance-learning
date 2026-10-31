import streamlit as st

def loss_ratio(premium, claims):
    """Calculate the loss ratio given premium and claims."""
    return claims / premium

def combined_ratio(claims, expenses, premium):
    """Calculate the combined ratio given claims, expenses, and premium."""
    return (claims + expenses) / premium

st.title("Underwriting Ratio Calculator")

premium = st.number_input("Enter premium amount ($):", min_value=0.0, step=1000.0)
claims = st.number_input("Enter claims amount ($):", min_value=0.0, step=1000.0)
expenses = st.number_input("Enter expenses amount ($):", min_value=0.0, step=1000.0)

loss = loss_ratio(premium, claims)
combined = combined_ratio(claims, expenses, premium)

st.write(f"Loss Ratio: {loss:.2%}")
st.write(f"Combined Ratio: {combined:.2%}") 

if combined > 1:
    st.warning("Combined ratio is above 100%. Consider reviewing underwriting practices or reinsurance arrangements.")
else:
    st.success("Underwriting profit")

cession_rate = st.slider("Select cession rate (%):", min_value=0.0, max_value=100.0, value=30.0, step=1.0) / 100.0
ceded_premium = premium * cession_rate
st.metric("Ceded Premium", f"${ceded_premium:,.0f}")