import streamlit as st
from mortgage_data import get_mock_mortgage_rates

st.title("🏡 Mortgage Interest Rate Comparison Tool")
st.markdown("Find the best mortgage deals based on rate type, term, and LTV.")

df = get_mock_mortgage_rates()

# Filters
rate_type = st.selectbox("Choose Rate Type", df['rate_type'].unique())
term = st.selectbox("Select Term", df['term'].unique())
ltv = st.selectbox("Select LTV", df['ltv'].unique())

filtered_df = df[
    (df['rate_type'] == rate_type) &
    (df['term'] == term) &
    (df['ltv'] == ltv)
]

# Sort by lowest rate first
sorted_df = filtered_df.sort_values(by="rate")

st.subheader("💡 Matching Mortgage Products")
st.dataframe(sorted_df)

loan_amount = st.number_input("Enter Mortgage Amount (£)", value=200000)

def calculate_monthly_payment(rate, years, amount):
    monthly_rate = rate / 100 / 12
    n_payments = years * 12
    if monthly_rate == 0:
        return amount / n_payments
    return (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -n_payments)

if not sorted_df.empty:
    selected = sorted_df.iloc[0]
    # UK mortgage amortization default is 25 years
    amortization_years = 25
    monthly_payment = calculate_monthly_payment(selected['rate'], years, loan_amount)
    st.metric("💸 Estimated Monthly Payment", f"£{monthly_payment:.2f}")
