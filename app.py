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

# Idaho state income tax settings
standard_deduction = 15000  # single filer; change if needed
idaho_tax_rate = 0.05695    # 5.695%

records = []
for day in range(days):
    visitors = daily_visitors[day]
    orders = np.random.poisson(visitors * conversion_rate)  # randomness in orders
    revenue = orders * price
    cost_goods = orders * cost
    payment_fees = orders * (price * 0.029 + 0.30)
    amazon_fees = revenue * 0.15
    domain_fee = 15 / 365
    refunds = np.random.binomial(orders, refund_rate)
    refund_cost = refunds * price

    # Profit before taxes
    pre_tax_profit = revenue - cost_goods - payment_fees - amazon_fees - ad_spend - refund_cost - domain_fee

    # Idaho taxable income (apply deduction once, not daily)
    taxable_income = max(0, pre_tax_profit - (standard_deduction / days))  # spread deduction over 30 days
    idaho_income_tax = taxable_income * idaho_tax_rate

    # Net profit after Idaho tax
    net_profit = pre_tax_profit - idaho_income_tax

    records.append([day+1, visitors, orders, revenue, cost_goods, payment_fees, amazon_fees, domain_fee, ad_spend, refund_cost, idaho_income_tax, net_profit])

# DataFrame
df = pd.DataFrame(records, columns=[
    "Day", "Visitors", "Orders", "Revenue", "Cost of Goods", "Payment Fees", 
    "Amazon Fees", "Domain Fee", "Ad Spend", "Refund Cost", "Idaho Income Tax", "Net Profit"
])

# Totals row
totals = df[[
    "Revenue", "Cost of Goods", "Payment Fees", "Amazon Fees", "Domain Fee", 
    "Ad Spend", "Refund Cost", "Idaho Income Tax", "Net Profit"
]].sum()
totals["Day"] = "TOTAL"
df_totals = pd.DataFrame(totals).T

# Display
st.dataframe(pd.concat([df, df_totals], ignore_index=True))
st.line_chart(df.set_index("Day")["Net Profit"], use_container_width=True)

# Chart
st.line_chart(df.set_index("Day")["Net Profit"], use_container_width=True)
