# Power BI dashboard specification

## Data source
Run `src/analyze.py`; import `credit_risk_clean.csv` as `credit_risk`. Confirm `loan_status` is whole number and `loan_int_rate` is numeric. Set default rate DAX measure format to Percentage.

## Page 1 — Portfolio overview
- KPI cards: Labeled Applications, Defaults, Default Rate %, Average Loan Amount
- Bar chart: application count and default rate by loan grade
- Line or column chart: default rate by loan purpose
- Slicers: loan grade, loan intent, home ownership, income band

## Page 2 — Borrower and affordability segments
- Default rate by income band and loan-to-income burden
- Distribution of loan amount and interest rate
- Matrix: loan grade × loan purpose with application count and default rate

## Page 3 — Data quality
- Missing values by field from `data_quality.csv`
- Count of unlabeled rows and duplicate rows from `overall_kpis.csv`

## Design rules
Show denominators with percentages, indicate dataset period/source, use consistent number formats, and label findings as descriptive associations. Avoid implying that any field causes default.
