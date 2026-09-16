import pandas as pd

df = pd.read_csv("data/cleaned_superstore.csv")

top_region = df.groupby("Region")["Sales"].sum().idxmax()

top_category = df.groupby("Category")["Profit"].sum().idxmax()

top_segment = df.groupby("Segment")["Sales"].sum().idxmax()

monthly_sales = df.groupby(
    pd.to_datetime(df["Order Date"]).dt.to_period("M")
)["Sales"].sum()

best_month = monthly_sales.idxmax()

print("\n===== AI BUSINESS INSIGHTS =====")

print(f"Top Region: {top_region}")

print(f"Highest Profit Category: {top_category}")

print(f"Largest Customer Segment: {top_segment}")

print(f"Best Sales Month: {best_month}")

print("\n===== RECOMMENDATIONS =====")

print("Increase marketing in low-performing regions.")

print("Focus on high-profit categories.")

print("Monitor monthly sales trends.")