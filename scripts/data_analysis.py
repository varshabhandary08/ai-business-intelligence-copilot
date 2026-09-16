import pandas as pd

# Load dataset
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

# Convert date columns
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# =====================
# BUSINESS KPIs
# =====================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
avg_order_value = total_sales / total_orders

print("===== BUSINESS KPIs =====")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Average Order Value: ${avg_order_value:,.2f}")

# =====================
# SALES BY REGION
# =====================

region_sales = (
    df.groupby("Region")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== SALES BY REGION =====")
print(region_sales)
# =====================
# PROFIT BY REGION
# =====================

region_profit = (
    df.groupby("Region")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== PROFIT BY REGION =====")
print(region_profit)
# =====================
# SALES BY CATEGORY
# =====================

category_sales = (
    df.groupby("Category")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== SALES BY CATEGORY =====")
print(category_sales)
# =====================
# PROFIT BY CATEGORY
# =====================

category_profit = (
    df.groupby("Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== PROFIT BY CATEGORY =====")

for category, profit in category_profit.items():
    print(f"{category}: ${profit:,.2f}")
    # =====================
# TOP 10 PRODUCTS BY SALES
# =====================

top_products = (
    df.groupby("Product Name")["Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\n===== TOP 10 PRODUCTS BY SALES =====")
print(top_products)
# =====================
# MONTHLY SALES TREND
# =====================

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
      .sum()
)

print("\n===== MONTHLY SALES TREND =====")
print(monthly_sales)
# =====================
# TOP 10 PRODUCTS BY PROFIT
# =====================

top_profit_products = (
    df.groupby("Product Name")["Profit"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\n===== TOP 10 PRODUCTS BY PROFIT =====")
print(top_profit_products)
# =====================
# SALES BY CUSTOMER SEGMENT
# =====================

segment_sales = (
    df.groupby("Segment")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\n===== SALES BY CUSTOMER SEGMENT =====")
print(segment_sales)