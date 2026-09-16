import pandas as pd

# Load dataset
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Save cleaned data
df.to_csv("data/cleaned_superstore.csv", index=False)

print("Cleaned dataset exported successfully!")