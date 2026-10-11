"""
Data Cleaning & Visualization Project
--------------------------------------
Cleans a raw retail sales dataset (handles missing values, duplicates,
outliers) and generates visual reports / a summary dashboard.

Author: (your name here)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

RAW_PATH = "data/raw_sales_data.csv"
CLEAN_PATH = "outputs/cleaned_sales_data.csv"

# ---------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------
df = pd.read_csv(RAW_PATH, parse_dates=["Date"])
print("Raw shape:", df.shape)
print("\nMissing values before cleaning:\n", df.isnull().sum())

# ---------------------------------------------------------------
# 2. HANDLE DUPLICATES
# ---------------------------------------------------------------
dupe_count = df.duplicated(subset=[c for c in df.columns if c != "OrderID"]).sum()
print(f"\nDuplicate rows found (ignoring OrderID): {dupe_count}")
df = df.drop_duplicates(subset=[c for c in df.columns if c != "OrderID"])

# ---------------------------------------------------------------
# 3. HANDLE MISSING VALUES
# ---------------------------------------------------------------
# Region: fill missing with "Unknown"
df["Region"] = df["Region"].fillna("Unknown")

# Price: fill missing with median price of that Category
df["Price"] = df.groupby("Category")["Price"].transform(
    lambda x: x.fillna(x.median())
)

# CustomerAge: fill missing with overall median age
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())

# Rating: fill missing with mode (most common rating)
df["Rating"] = df["Rating"].fillna(df["Rating"].mode()[0])

# ---------------------------------------------------------------
# 4. HANDLE OUTLIERS
# ---------------------------------------------------------------
# CustomerAge: realistic bounds
df = df[(df["CustomerAge"] >= 15) & (df["CustomerAge"] <= 90)]

# Price: cap using IQR method
Q1, Q3 = df["Price"].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
before = df.shape[0]
df["Price"] = df["Price"].clip(lower=lower, upper=upper)
print(f"\nPrice outliers capped using IQR bounds [{lower:.2f}, {upper:.2f}]")

# ---------------------------------------------------------------
# 5. STANDARDIZE / FEATURE ENGINEERING
# ---------------------------------------------------------------
df["Region"] = df["Region"].str.title()
df["Month"] = df["Date"].dt.month_name()
df["Revenue"] = df["Price"] * df["Quantity"]

df = df.reset_index(drop=True)
df.to_csv(CLEAN_PATH, index=False)
print("\nCleaned shape:", df.shape)
print("Missing values after cleaning:\n", df.isnull().sum())
print(f"\nSaved cleaned dataset -> {CLEAN_PATH}")

# ---------------------------------------------------------------
# 6. VISUALIZATIONS / DASHBOARD
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(20, 11))
fig.suptitle("Sales Data Cleaning & Visualization Dashboard", fontsize=18, fontweight="bold")

# 6.1 Revenue by Category
cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
sns.barplot(x=cat_rev.values, y=cat_rev.index, ax=axes[0, 0], palette="viridis")
axes[0, 0].set_title("Total Revenue by Category")
axes[0, 0].set_xlabel("Revenue")

# 6.2 Revenue by Region
reg_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
sns.barplot(x=reg_rev.index, y=reg_rev.values, ax=axes[0, 1], palette="magma")
axes[0, 1].set_title("Total Revenue by Region")
axes[0, 1].tick_params(axis='x', rotation=30)

# 6.3 Price distribution (after outlier handling)
sns.histplot(df["Price"], bins=25, kde=True, ax=axes[0, 2], color="steelblue")
axes[0, 2].set_title("Price Distribution (Cleaned)")

# 6.4 Monthly revenue trend
month_order = ["January","February","March","April","May","June",
                "July","August","September","October","November","December"]
month_rev = df.groupby("Month")["Revenue"].sum().reindex(month_order)
axes[1, 0].plot(month_rev.index, month_rev.values, marker="o", color="darkorange")
axes[1, 0].set_title("Monthly Revenue Trend")
axes[1, 0].tick_params(axis='x', rotation=45)

# 6.5 Rating distribution
sns.countplot(x="Rating", data=df, ax=axes[1, 1], palette="crest")
axes[1, 1].set_title("Customer Rating Distribution")

# 6.6 Age vs Revenue scatter
sns.scatterplot(x="CustomerAge", y="Revenue", hue="Category", data=df, ax=axes[1, 2], alpha=0.7)
axes[1, 2].set_title("Customer Age vs Revenue")
axes[1, 2].legend(fontsize=7)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("outputs/dashboard.png", dpi=150)
print("Saved dashboard -> outputs/dashboard.png")
plt.close()

# ---------------------------------------------------------------
# 7. TEXT SUMMARY REPORT
# ---------------------------------------------------------------
with open("outputs/summary_report.txt", "w") as f:
    f.write("DATA CLEANING & VISUALIZATION - SUMMARY REPORT\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Rows before cleaning : {before}\n")
    f.write(f"Rows after cleaning  : {df.shape[0]}\n")
    f.write(f"Duplicates removed   : {dupe_count}\n\n")
    f.write("Top category by revenue: {}\n".format(cat_rev.idxmax()))
    f.write("Top region by revenue  : {}\n".format(reg_rev.idxmax()))
    f.write(f"Average order value    : {df['Revenue'].mean():.2f}\n")
    f.write(f"Average customer rating: {df['Rating'].mean():.2f}\n")

print("Saved summary -> outputs/summary_report.txt")
