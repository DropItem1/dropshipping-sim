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

# Sliders (put these ONCE, before the loop)
tiktok_posts = st.slider("TikTok Posts per Day", 0, 5, 1, key="tiktok")
instagram_posts = st.slider("Instagram Posts per Day", 0, 5, 1, key="insta")
youtube_posts = st.slider("YouTube Posts per Day", 0, 5, 1, key="yt")

# Simulation
np.random.seed(42)
days = 30
daily_visitors = np.random.randint(40, 100, days)


# Idaho state income tax settings
standard_deduction = 14600  # single filer; change if needed
idaho_tax_rate = 0.05695    # 5.695%

records = []
for day in range(days):
    visitors = daily_visitors[day]

    tiktok_reach = sum(np.random.randint(15, 50) for _ in range(tiktok_posts))
    instagram_reach = sum(np.random.randint(5, 20) for _ in range(instagram_posts))
    youtube_reach = sum(np.random.randint(20, 60) for _ in range(youtube_posts))
    visitors += tiktok_reach + instagram_reach + youtube_reach

   # Orders and revenue
    orders = np.random.binomial(visitors, conversion_rate)
    revenue = orders * price
    cost_goods = orders * cost

    # Fees
    payment_fees = orders * (price * 0.029 + 0.30)
    amazon_fees = revenue * 0.15
    domain_fee = 15 / 365  

    # Refunds
    refunds = np.random.binomial(orders, refund_rate)
    refund_cost = refunds * price

    # Profit before tax
    pre_tax_profit = revenue - cost_goods - payment_fees - amazon_fees - ad_spend - refund_cost - domain_fee

    # Idaho income tax (flat 5.695%)
    idaho_income_tax = pre_tax_profit * 0.05695 if pre_tax_profit > 0 else 0

    # Net profit after tax
    net_profit = pre_tax_profit - idaho_income_tax

    # Save daily record
    records.append([
        day+1,
        visitors,
        orders,
        revenue,
        cost_goods,
        payment_fees,
        amazon_fees,
        domain_fee,
        ad_spend,
        refund_cost,
        idaho_income_tax,
        net_profit
    ])

# DataFrame
df = pd.DataFrame(records, columns=[
    "Day", "Visitors", "Orders", "Revenue", "Cost of Goods", "Payment Fees", 
    "Amazon Fees", "Domain Fee", "Ad Spend", "Refund Cost", "Pre-Tax Profit"
])

# Totals across all days
totals = df[[
    "Revenue", "Cost of Goods", "Payment Fees", "Amazon Fees", "Domain Fee", 
    "Ad Spend", "Refund Cost", "Pre-Tax Profit"
]].sum()

# Annual Idaho income tax
annual_pre_tax_profit = totals["Pre-Tax Profit"]
standard_deduction = 14600  

if annual_pre_tax_profit > standard_deduction:
    taxable_income = annual_pre_tax_profit - standard_deduction
    idaho_income_tax = taxable_income * 0.05695
else:
    idaho_income_tax = 0

net_profit_after_tax = annual_pre_tax_profit - idaho_income_tax

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

# Each platform’s reach factor (random range per post)
tiktok_reach = [np.random.randint(15, 50) for _ in range(tiktok_posts)]
instagram_reach = [np.random.randint(5, 20) for _ in range(instagram_posts)]
youtube_reach = [np.random.randint(20, 60) for _ in range(youtube_posts)]

# Total social media visitors
social_visitors = sum(tiktok_reach) + sum(instagram_reach) + sum(youtube_reach)

# Daily visitors
visitors = daily_visitors[day] + social_visitors
