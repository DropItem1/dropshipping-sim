import streamlit as st
import numpy as np
import pandas as pd

st.title("📦 Dropshipping Business Simulator")

st.write("Adjust your business settings and see how your dropshipping store performs over 30 days.")

# -----------------------------
# User inputs
# -----------------------------
price = st.slider("Selling Price per Item ($)", 10, 50, 22)
cost = st.slider("Supplier Cost per Item ($)", 2, 20, 6)
ad_spend = st.slider("Daily Ad Spend ($)", 0, 50, 10)
conversion_rate = st.slider("Conversion Rate (%)", 1.0, 10.0, 2.5) / 100
refund_rate = st.slider("Refund Rate (%)", 0.0, 20.0, 5.0) / 100

# Social media sliders
tiktok_posts = st.slider("TikTok Posts per Day", 0, 5, 1, key="tiktok")
instagram_posts = st.slider("Instagram Posts per Day", 0, 5, 1, key="insta")
youtube_posts = st.slider("YouTube Posts per Day", 0, 5, 1, key="yt")

# -----------------------------
# Simulation setup
# -----------------------------
np.random.seed(42)
days = 30
daily_visitors = np.random.randint(40, 100, days)

records = []

for day in range(days):
    # Base visitors
    visitors = daily_visitors[day]

    # Social media reach
    tiktok_reach = sum(np.random.randint(15, 50) for _ in range(tiktok_posts))
    instagram_reach = sum(np.random.randint(5, 20) for _ in range(instagram_posts))
    youtube_reach = sum(np.random.randint(20, 60) for _ in range(youtube_posts))
    visitors += tiktok_reach + instagram_reach + youtube_reach

    # Orders & revenue
    orders = np.random.binomial(visitors, conversion_rate)
    revenue = orders * price
    cost_goods = orders * cost

    # Fees
    payment_fees = orders * (price * 0.029 + 0.30)
    amazon_fees = revenue * 0.15
    domain_fee = 15 / 365  # daily domain fee

    # Refunds
    refunds = np.random.binomial(orders, refund_rate)
    refund_cost = refunds * price

    # Profit before tax
    pre_tax_profit = (
        revenue - cost_goods - payment_fees - amazon_fees - ad_spend - refund_cost - domain_fee
    )

    # Save daily record (11 values, matches 11 columns)
    records.append([
        day + 1,
        visitors,
        orders,
        revenue,
        cost_goods,
        payment_fees,
        amazon_fees,
        domain_fee,
        ad_spend,
        refund_cost,
        pre_tax_profit
    ])

# -----------------------------
# DataFrame
# -----------------------------
df = pd.DataFrame(records, columns=[
    "Day", "Visitors", "Orders", "Revenue", "Cost of Goods", "Payment Fees",
    "Amazon Fees", "Domain Fee", "Ad Spend", "Refund Cost", "Pre-Tax Profit"
])

# -----------------------------
# Totals and Idaho tax (annual)
# -----------------------------
totals = df[[
    "Revenue", "Cost of Goods", "Payment Fees", "Amazon Fees", "Domain Fee",
    "Ad Spend", "Refund Cost", "Pre-Tax Profit"
]].sum()

annual_pre_tax_profit = totals["Pre-Tax Profit"]
standard_deduction = 14600  # single filer
idaho_tax_rate = 0.05695    # 5.695%

if annual_pre_tax_profit > standard_deduction:
    taxable_income = annual_pre_tax_profit - standard_deduction
    idaho_income_tax = taxable_income * idaho_tax_rate
else:
    taxable_income = 0
    idaho_income_tax = 0

net_profit_after_tax = annual_pre_tax_profit - idaho_income_tax

# -----------------------------
# Display
# -----------------------------
st.dataframe(df)

st.write("### Totals (30 Days)")
st.write(totals)

st.write(f"**Idaho Income Tax:** ${idaho_income_tax:,.2f}")
st.write(f"**Net Profit After Tax:** ${net_profit_after_tax:,.2f}")

st.line_chart(df.set_index("Day")["Pre-Tax Profit"], use_container_width=True)
