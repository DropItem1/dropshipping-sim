records = []
for day in range(days):
    visitors = daily_visitors[day]

    # Social media reach
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

    # Idaho income tax (flat 5.695% daily portion, only if profitable)
    standard_deduction = 14600 / days
    taxable_income = max(0, pre_tax_profit - standard_deduction)
    idaho_income_tax = taxable_income * 0.05695

    # Net profit after tax
    net_profit = pre_tax_profit - idaho_income_tax

    # Save record
    records.append([
        day+1, visitors, orders, revenue, cost_goods, payment_fees,
        amazon_fees, domain_fee, ad_spend, refund_cost, idaho_income_tax, net_profit
    ])

# DataFrame AFTER loop
df = pd.DataFrame(records, columns=[
    "Day", "Visitors", "Orders", "Revenue", "Cost of Goods", "Payment Fees", 
    "Amazon Fees", "Domain Fee", "Ad Spend", "Refund Cost", "Idaho Income Tax", "Net Profit"
])
