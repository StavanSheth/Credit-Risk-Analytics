# Credit Risk & Loan Default Analytics

A reproducible intermediate-level portfolio project using SQL, Python and Power BI.

## Dataset
Download the public Kaggle **Credit Risk Dataset**: https://www.kaggle.com/datasets/laotse/credit-risk-dataset
Place `credit_risk_dataset.csv` in `data/raw/`. Do not commit the full dataset unless its license permits redistribution.

## Questions
- How does default rate vary by loan grade, purpose, home ownership and income?
- What share of applicants have high loan-to-income burden?
- How do loan amount and interest rate vary by risk grade?
- Are missing values or implausible values concentrated in particular fields?

## Run (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate  | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py --input data/raw/credit_risk_dataset.csv --output data/processed
```
The script validates required columns, reports data-quality issues, cleans conservative invalid values, calculates descriptive KPIs and exports CSV tables for Power BI. It does not train a model or claim causal relationships.

## SQL
`sql/` contains SQLite-compatible table definitions and analysis queries. Run after loading the cleaned CSV into a table named `credit_risk`.

## Power BI
Import `data/processed/` outputs after running the script. Use `powerbi/measures.dax` for measures and `powerbi/dashboard_spec.md` for page layout. A `.pbix` is a Power BI Desktop binary and must be saved from Power BI Desktop; this repository provides the reproducible sources, not a prebuilt binary.

## Interpretation & responsible use
This is an educational analysis of a public dataset, not a credit underwriting system. Dataset labels, sampling and definitions may not represent a real lender's portfolio. Do not use the results to make real lending decisions.
