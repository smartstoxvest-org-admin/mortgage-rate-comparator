
import streamlit as st
import pandas as pd
import plotly.express as px
from mortgage_data import get_mock_mortgage_rates

st.set_page_config(page_title="Mortgage Tool", page_icon="🏡")
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

sorted_df = filtered_df.sort_values(by="rate")

if sorted_df.empty:
    st.warning("😕 No matching mortgage products found. Try adjusting the filters.")
else:
    st.subheader("💡 Matching Mortgage Products")
    st.dataframe(sorted_df)

    st.subheader("📊 Interest Rate Comparison Chart")

    fig = px.bar(
        sorted_df,
        x="bank",
        y="rate",
        color="rate",
        text="rate",
        title=f"Interest Rates for {rate_type} Mortgages ({term}, {ltv})",
        labels={"rate": "Interest Rate (%)"},
        hover_data=["term", "ltv", "fee"],
        height=400
    )

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(yaxis=dict(range=[0, sorted_df['rate'].max() + 1]))

    st.plotly_chart(fig, use_container_width=True)

    # Mortgage Calculator
    loan_amount = st.number_input("Enter Mortgage Amount (£)", value=200000)
    amortization_years = st.slider("Select Mortgage Repayment Term (Years)", 5, 40, 25)

    def calculate_monthly_payment(rate, years, amount):
        monthly_rate = rate / 100 / 12
        n_payments = years * 12
        if monthly_rate == 0:
            return amount / n_payments
        return (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -n_payments)

    selected = sorted_df.iloc[0]
    monthly_payment = calculate_monthly_payment(selected['rate'], amortization_years, loan_amount)
    st.success(f"💸 Estimated Monthly Payment: £{monthly_payment:.2f}")
