import streamlit as st
import plotly.express as px

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
if not sorted_df.empty:
    st.subheader("📊 Interest Rate Comparison Chart")

    fig = px.bar(
        sorted_df,
        x="bank",
        y="rate",
        color="rate",
        text="rate",
        title="Interest Rates by Bank",
        labels={"rate": "Interest Rate (%)"},
        height=400
    )

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(yaxis=dict(range=[0, sorted_df['rate'].max() + 1]))

    st.plotly_chart(fig, use_container_width=True)

loan_amount = st.number_input("Enter Mortgage Amount (£)", value=200000)

def calculate_monthly_payment(rate, years, amount):
    monthly_rate = rate / 100 / 12
    n_payments = years * 12
    if monthly_rate == 0:
        return amount / n_payments
    return (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -n_payments)

if not sorted_df.empty:
    selected = sorted_df.iloc[0]
    amortization_years = st.slider("Select Mortgage Repayment Term (Years)", 5, 40, 25)
    monthly_payment = calculate_monthly_payment(selected['rate'], amortization_years, loan_amount)
    st.metric("💸 Estimated Monthly Payment", f"£{monthly_payment:.2f}")

