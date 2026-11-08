
from pathlib import Path
import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Project paths and folders
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"
CHARTS = OUTPUTS / "charts"

for folder in [PROCESSED, OUTPUTS, CHARTS]:
    folder.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load raw dataset
# --------------------------------------------------

file_path = RAW / "superstore.csv"

if not file_path.exists():
    raise FileNotFoundError(
        "Dataset not found. Run scripts/download_data.py first."
    )

df = pd.read_csv(
    file_path,
    sep="\t",
    encoding="utf-16",
    header=None,
    skiprows=1,
    names=[
        "Profit_Ratio",
        "ONE",
        "Category",
        "City",
        "Country",
        "Customer_Name",
        "Discount",
        "Number_of_Records",
        "Order_Date",
        "Order_ID",
        "Postal_Code",
        "Manufacturer",
        "Product_Name",
        "Profit",
        "Quantity",
        "Region",
        "Sales",
        "Segment",
        "Ship_Date",
        "Ship_Mode",
        "State",
        "Sub_Category"
    ]
)

original_records = len(df)


# --------------------------------------------------
# 3. Validate required columns
# --------------------------------------------------

df.columns = [
    col.strip().replace(" ", "_")
    for col in df.columns
]

required = [
    "Order_ID",
    "Order_Date",
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Region",
    "Category",
    "Sub_Category"
]

missing = set(required) - set(df.columns)

if missing:
    raise ValueError(
        f"Missing required columns: {missing}"
    )


# --------------------------------------------------
# 4. Data cleaning and type conversion
# --------------------------------------------------

# Clean sales and profit currency values
for col in ["Sales", "Profit"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(r"[$,]", "", regex=True)
        .str.strip()
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# Convert discount percentages to decimals
df["Discount"] = (
    df["Discount"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)

df["Discount"] = (
    pd.to_numeric(
        df["Discount"],
        errors="coerce"
    ) / 100
)


# Convert quantity to numeric
df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)


# Convert dates
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["Ship_Date"] = pd.to_datetime(
    df["Ship_Date"],
    errors="coerce"
)


# Remove records missing essential fields
df = df.dropna(
    subset=[
        "Order_ID",
        "Order_Date",
        "Sales",
        "Profit",
        "Quantity",
        "Discount",
        "Region",
        "Category",
        "Sub_Category"
    ]
).copy()


# Validate cleaned dataset
if df.empty:
    raise ValueError(
        "No valid records remain after data cleaning."
    )

if df["Sales"].sum() == 0:
    raise ValueError(
        "Total sales are zero. Profit margin cannot be calculated."
    )


# --------------------------------------------------
# 5. Feature engineering
# --------------------------------------------------

df["Order_Month"] = (
    df["Order_Date"]
    .dt.to_period("M")
    .astype(str)
)

df["Profit_Margin"] = (
    df["Profit"] /
    df["Sales"].where(df["Sales"] != 0)
)


# --------------------------------------------------
# 6. Export cleaned dataset
# --------------------------------------------------

df.to_csv(
    PROCESSED / "retail_orders_clean.csv",
    index=False
)


# --------------------------------------------------
# 7. Regional performance analysis
# --------------------------------------------------

region = (
    df.groupby("Region")
    .agg(
        Orders=("Order_ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

region["Profit_Margin"] = (
    region["Profit"] / region["Sales"]
)

region.to_csv(
    OUTPUTS / "retail_region_summary.csv",
    index=False
)


# --------------------------------------------------
# 8. Monthly performance analysis
# --------------------------------------------------

monthly = (
    df.groupby("Order_Month")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
    .sort_values("Order_Month")
)

monthly.to_csv(
    OUTPUTS / "retail_monthly_summary.csv",
    index=False
)


# --------------------------------------------------
# 9. Sub-category profitability analysis
# --------------------------------------------------

subcategory = (
    df.groupby("Sub_Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Profit")
    .reset_index()
)

subcategory.to_csv(
    OUTPUTS / "retail_subcategory_summary.csv",
    index=False
)


# --------------------------------------------------
# 10. Monthly sales visualization
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    monthly["Order_Month"],
    monthly["Sales"],
    marker="o"
)

ax.set_title("Monthly Sales Performance")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")

plt.xticks(rotation=60)
plt.tight_layout()

plt.savefig(
    CHARTS / "monthly_sales.png",
    dpi=160
)

plt.close()


# --------------------------------------------------
# 11. Sub-category profitability visualization
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 6))

top = subcategory.tail(10)

ax.barh(
    top["Sub_Category"],
    top["Profit"]
)

ax.set_title("Top 10 Profitable Sub-Categories")
ax.set_xlabel("Profit")

plt.tight_layout()

plt.savefig(
    CHARTS / "top_profit_subcategories.png",
    dpi=160
)

plt.close()


# --------------------------------------------------
# 12. Export SQLite database
# --------------------------------------------------

database = OUTPUTS / "retail_analysis.db"

with sqlite3.connect(database) as connection:
    df.to_sql(
        "orders",
        connection,
        if_exists="replace",
        index=False
    )


# --------------------------------------------------
# 13. Final business performance summary
# --------------------------------------------------

total_orders = df["Order_ID"].nunique()
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

profit_margin = (
    total_profit / total_sales
) * 100

print("\n========== DATA CLEANING SUMMARY ==========")
print(f"Original records: {original_records}")
print(f"Clean records: {len(df)}")
print(f"Records removed: {original_records - len(df)}")

print("\n========== BUSINESS PERFORMANCE ==========")
print(f"Total Orders: {total_orders}")
print(f"Total Sales: ${total_sales:,.0f}")
print(f"Total Profit: ${total_profit:,.0f}")
print(f"Profit Margin: {profit_margin:.2f}%")

print("\n========== OUTPUT FILES ==========")
print("Clean dataset: data/processed/retail_orders_clean.csv")
print("SQLite database: outputs/retail_analysis.db")
print("Regional summary: outputs/retail_region_summary.csv")
print("Monthly summary: outputs/retail_monthly_summary.csv")
print("Subcategory summary: outputs/retail_subcategory_summary.csv")
print("Charts: outputs/charts/")

print("\nAnalysis completed successfully.")
