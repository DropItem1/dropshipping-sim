import streamlit as st
import numpy as np
import pandas as pd

st.title("📦 Dropshipping Business Simulator (1 Year)")

st.write("Simulates 365 days of your dropshipping business. Adjust inputs and see how performance changes.")

# -----------------------------
# User inputs
# -----------------------------
price = st.slider("Selling Price per Item ($)", 10, 100, 25)
cost = st.slider("Supplier Cost per Item ($)", 2, 40, 8)
ad_spend = st.slider("Daily Ad Spend ($)", 0, 100, 15)
conversion_rate = st.slider("Conversion Rate (%)", 0.5, 10.0, 2.0) / 100
refund_rate = st.slider("Refund Rate (%)", 0.0, 20.0, 3.0) / 100

# Social media sliders
tiktok_posts = st.slider("TikTok Posts per Day", 0, 10, 2, key="tiktok")
instagram_posts = st.slider("Instagram Posts per Day", 0, 10, 1, key="insta")
youtube_posts = st.slider("YouTube Posts per Day", 0, 5, 0, key="yt")

# -----------------------------
# Simulation setup
# -----------------------------
np.random.seed(42)
days = 365  # simulate full year

# base daily visitors (ads + randomness)
daily_visitors = np.random.randint(30, 120, days)

records = []

for day in range(days):
    visitors = daily_visitors[day]

    # Social media reach effect (random but scales with posts)
    tiktok_reach = sum(np.random.randint(10, 80) for _ in range(tiktok_posts))
    instagram_reach = sum(np.random.randint(5, 30) for _ in range(instagram_posts))
    youtube_reach = sum(np.random.randint(15, 100) for _ in range(youtube_posts))

    visitors += tiktok_reach + instagram_reach + youtube_reach

     # Orders & revenue
    # Add chance of no-sale day (e.g., 15% chance)
    if np.random.rand() < 0.40:
        orders = 0
    else:
        orders = np.random.binomial(visitors, conversion_rate)

    revenue = orders * price
    cost_goods = orders * cost

    # Fees
    payment_fees = orders * (price * 0.029 + 0.30)
    amazon_fees = revenue * 0.15
    individual_fee = orders * 1.00
    domain_fee = 15 / 365  # daily domain fee

    # Refunds
    refunds = np.random.binomial(orders, refund_rate)
    refund_cost = refunds * price

    # Profit before tax
pre_tax_profit = (
    revenue - cost_goods - payment_fees - amazon_fees - individual_fee
    - ad_spend - refund_cost - domain_fee
)

    # Save daily record
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
        pre_tax_profit,
        individual_fee
    ])

# -----------------------------
# DataFrame
# -----------------------------
df = pd.DataFrame(records, columns=[
    "Day", "Visitors", "Orders", "Revenue", "Cost of Goods", "Payment Fees",
    "Amazon Fees", "Domain Fee", "Ad Spend", "Refund Cost", "Pre-Tax Profit", "Individual Fee"
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

st.write("### Totals (365 Days)")
st.write(totals)

st.write(f"**Idaho Income Tax:** ${idaho_income_tax:,.2f}")
st.write(f"**Net Profit After Tax:** ${net_profit_after_tax:,.2f}")

st.line_chart(df.set_index("Day")["Pre-Tax Profit"], use_container_width=True)
