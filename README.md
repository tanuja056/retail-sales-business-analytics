# Retail Sales & Business Performance Analytics

An end-to-end business analytics project using Python, SQL, SQLite, and Power BI to analyze retail sales, profitability, regional performance, product categories, and discount patterns.

## Project Overview

This project analyzes a retail Superstore dataset containing 9,994 records across multiple regions, product categories, customers, and order dates.

The objective is to transform raw retail data into actionable business insights through data cleaning, exploratory analysis, SQL queries, and interactive Power BI visualizations.

## Technology Stack

- **Python:** Pandas, NumPy, Matplotlib
- **SQL:** Business analysis queries
- **Database:** SQLite
- **Visualization:** Power BI, Matplotlib
- **Development:** VS Code, Git, GitHub

## Project Workflow

1. Download and ingest the raw dataset.
2. Clean and validate the data using Python.
3. Engineer analytical features, including monthly order periods and profit margins.
4. Export the cleaned dataset and analytical summaries.
5. Load the cleaned data into SQLite.
6. Execute SQL queries to investigate business performance.
7. Build an interactive Power BI dashboard.

## Repository Structure

```text
retail-sales-business-analytics/
│
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   └── processed/
│       └── retail_orders_clean.csv
│
├── scripts/
│   ├── download_data.py
│   ├── run_analysis.py
│   └── run_sql.py
│
├── sql/
│   └── retail_analysis.sql
│
├── powerbi/
│   └── retail_sales_dashboard.pbix
│
├── outputs/
│   ├── charts/
│   ├── retail_analysis.db
│   ├── retail_monthly_summary.csv
│   ├── retail_region_summary.csv
│   └── retail_subcategory_summary.csv
│
├── notebooks/
├── README.md
├── requirements.txt
└── .gitignore
```

## Key Business Results

| Metric | Result |
|---|---:|
| Total records analyzed | 9,994 |
| Distinct orders | 5,009 |
| Total sales | $2,297,354 |
| Total profit | $286,347 |
| Overall profit margin | 12.46% |

## Business Insights

### 1. Regional Performance

- West generated the highest sales at $725,514 and the highest profit at $108,386.
- East generated $678,834 in sales and $91,521 in profit.
- Central had the lowest regional profit margin at approximately 7.92%.
- South generated $391,750 in sales and $46,721 in profit.

**Business recommendation:** Investigate Central's product mix and discounting patterns to identify opportunities to improve profitability.

### 2. Product Profitability

The three loss-making subcategories were:

| Subcategory | Profit |
|---|---:|
| Tables | -$17,733 |
| Bookcases | -$3,479 |
| Supplies | -$1,187 |

The most profitable subcategories included:

- Copiers: $55,618
- Phones: $44,492
- Accessories: $41,932

**Business recommendation:** Investigate pricing, discounting, and product-level profitability in loss-making subcategories before making decisions about product availability.

### 3. Discount Impact Analysis

| Discount Band | Sales | Profit | Profit Margin |
|---|---:|---:|---:|
| No Discount | $1,088,020 | $320,946 | 29.50% |
| 1–20% | $846,572 | $100,785 | 11.91% |
| 21–40% | $234,129 | -$35,804 | -15.29% |
| Above 40% | $128,633 | -$99,580 | -77.41% |

**Business recommendation:** Review high-discount transactions and evaluate whether discount policies are supporting profitable sales.

These results show an association between higher discount bands and lower profitability. They do not establish causation; product mix and other factors may also influence the results.

### 4. Monthly Sales Trends

- The analysis covers January 2015 through December 2018.
- November 2018 had the highest monthly sales at $118,456.
- February 2015 had the lowest monthly sales at $4,518.

## SQL Analysis

Five SQL analyses were developed:

1. Overall business performance.
2. Regional sales and profitability.
3. Monthly sales and profit trends.
4. Product subcategory profitability.
5. Discount band and profit margin analysis.

The SQL queries use aggregation, `GROUP BY`, `ORDER BY`, conditional logic, distinct counts, and calculated profit margins.

## Power BI Dashboard

The interactive dashboard includes:

- KPI cards for sales, profit, orders, profit margin, and quantity.
- Monthly sales trend.
- Regional sales and profitability comparison.
- Product subcategory profitability.
- Discount impact analysis.
- Region and category filters.

The Power BI dashboard is saved in the `powerbi/` directory.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/tanuja056/retail-sales-business-analytics.git
cd retail-sales-business-analytics
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the dataset

```bash
python scripts/download_data.py
```

### 5. Run Python analysis

```bash
python scripts/run_analysis.py
```

### 6. Run SQL analysis

```bash
python scripts/run_sql.py
```

The analysis generates a cleaned dataset, SQLite database, CSV summaries, and visualization files.

## Dataset and Limitations

The project uses the Sample Superstore dataset retrieved from a public GitHub mirror:

[Sample Superstore dataset source](https://github.com/mimansha98/Tableau_Dashboards)

The source data contains retail order-level records. Sales and profit values are represented as whole-dollar amounts in this version of the dataset.

This is a sample dataset, not proprietary company data. Findings are descriptive and should not be interpreted as causal conclusions.

## Future Improvements

- Customer retention and cohort analysis.
- More detailed customer-level profitability analysis.
- Automated data validation tests.
- Additional interactive Power BI measures and drill-through analysis.
- Predictive sales forecasting.

## Author

**Tanuja Kokkiligadda**

M.S. Data Science | University of Memphis

[LinkedIn](https://www.linkedin.com/in/tanuja-kokkiligadda) | [GitHub](https://github.com/tanuja056)
