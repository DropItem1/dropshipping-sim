import streamlit as st
import numpy as np
import pandas as pd

st.title("📦 Dropshipping Business Simulator")

st.write("Adjust your business settings and see how your dropshipping store performs over 30 days.")

# User inputs
price = st.slider("Selling Price per Item ($)", 10, 50, 22)
cost = st.slider("Supplier Cost per Item ($)", 2, 20, 6)
ad_spend = st.slider("Daily Ad Spend ($)", 0, 50, 10)
conversion_rate = st.slider("Conversion Rate (%)", 1.0, 10.0, 2.5) / 100
refund_rate = st.slider("Refund Rate (%)", 0.0, 20.0, 5.0) / 100

# Simulation
np.random.seed(42)
days = 30
daily_visitors = np.random.randint(40, 100, days)

records = []
for day in range(days):
    visitors = daily_visitors[day]
    orders = int(visitors * conversion_rate)
    revenue = orders * price
    cost_goods = orders * cost
    payment_fees = orders * (price * 0.029 + 0.30)
    amazon_fees = revenue * 0.15
    domain_fee = 15 / 365
    refunds = np.random.binomial(orders, refund_rate)
    refund_cost = refunds * price
    net_profit = revenue - cost_goods - payment_fees - amazon_fees - ad_spend - refund_cost - domain_fee
    records.append([
        day+1, visitors, orders, revenue,
        cost_goods, payment_fees, amazon_fees,
        domain_fee, ad_spend, refund_cost, net_profit
    ])
  # DataFrame
df = pd.DataFrame(records, columns=[
    "Day", "Visitors", "Orders", "Revenue",
    "Cost of Goods", "Payment Fees", "Amazon Fees",
    "Domain Fee", "Ad Spend", "Refund Cost", "Net Profit"
])
# Totals
totals = df[[
    "Revenue",
    "Cost of Goods",
    "Payment Fees",
    "Amazon Fees",
    "Domain Fee",
    "Ad Spend",
    "Refund Cost",
    "Net Profit"
]].sum()

totals["Day"] = "TOTAL"
df_totals = pd.DataFrame(totals).T

# Display results
st.dataframe(pd.concat([df, df_totals], ignore_index=True))

# Chart
st.line_chart(df.set_index("Day")["Net Profit"], use_container_width=True)
