from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# ==============================================================================
# BABY EXPLANATION:
# Imagine you have a giant Excel sheet of people asking for bank loans.
# Some people paid the bank back (loan_status = 0, good!),
# and some people didn't pay the bank back (loan_status = 1, default/bad!).
# This script inspects the data, cleans up silly mistakes (like negative age),
# calculates easy-to-understand stats, and saves nice summary tables.
# ==============================================================================

# This is our "Shopping List" / Checklist of columns that MUST be in our dataset.
# If any of these columns are missing, we stop and complain immediately!
REQUIRED = [
    "person_age",                 # How old the borrower is (e.g., 25 years old)
    "person_income",              # How much money they make in a year (e.g., $50,000)
    "person_home_ownership",      # Do they rent, own, or have a mortgage?
    "person_emp_length",          # How many years they have worked at their job
    "loan_intent",                # Why they want money (education, medical, personal...)
    "loan_grade",                 # Risk grade given by bank (A = safest, G = riskiest)
    "loan_amnt",                  # How much cash they are borrowing (e.g., $10,000)
    "loan_int_rate",              # Interest rate percentage (e.g., 11.5%)
    "loan_status",                # 0 = paid back successfully, 1 = defaulted (failed to pay)
    "loan_percent_income",        # Loan amount divided by income (burden ratio)
    "cb_person_default_on_file",  # Have they ever defaulted before? (Y/N)
    "cb_person_cred_hist_length", # How many years have they had a credit card/credit history
]


def main() -> None:
    # -------------------------------------------------------------------------
    # STEP 1: Understand what files the user wants to read and where to save results
    # -------------------------------------------------------------------------
    # Think of argparse like a receptionist asking: "Where is your file?" and "Where should I put the results?"
    p = argparse.ArgumentParser(description="Analyze the Kaggle credit risk dataset")
    p.add_argument("--input", required=True, help="Path to credit_risk_dataset.csv")
    p.add_argument("--output", default="data/processed", help="Output directory")
    args = p.parse_args()

    # Create the output folder if it doesn't already exist (so we don't get an error)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # STEP 2: Open and read the raw CSV data
    # -------------------------------------------------------------------------
    # pd.read_csv loads the comma-separated file into a tabular DataFrame (like an Excel sheet in memory).
    df = pd.read_csv(args.input)

    # Check if any required columns from our shopping list are missing
    missing_cols = sorted(set(REQUIRED) - set(df.columns))
    if missing_cols:
        raise SystemExit(f"Input schema mismatch; missing columns: {missing_cols}")

    # -------------------------------------------------------------------------
    # STEP 3: Check Data Quality (Health check of the data)
    # -------------------------------------------------------------------------
    # Before playing with the data, let's see how messy it is:
    # - Are there empty/blank spots (missing_count)?
    # - What percentage is blank (missing_pct)?
    # - How many different distinct answers are there (unique_values)?
    quality = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "missing_count": [int(df[c].isna().sum()) for c in df.columns],
        "missing_pct": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    # Save this health-check report to data_quality.csv
    quality.to_csv(out / "data_quality.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 4: Remove exact duplicates (Twin rows)
    # -------------------------------------------------------------------------
    # If the exact same person appears twice with identical information,
    # we don't want to count them twice! So we throw away identical copies.
    original_rows = len(df)
    df = df.drop_duplicates().copy()

    # -------------------------------------------------------------------------
    # STEP 5: Clean up crazy or impossible numbers
    # -------------------------------------------------------------------------
    # You cannot have an age of -5 or an income of -$100.
    # If we find numbers less than 0, we change them to NaN ("Not a Number" / blank)
    # so they don't mess up our math averages.
    for col in [
        "person_age", "person_income", "person_emp_length", "loan_amnt",
        "loan_int_rate", "loan_percent_income", "cb_person_cred_hist_length"
    ]:
        df.loc[df[col] < 0, col] = np.nan

    # loan_status must be either 0 (paid) or 1 (defaulted). Anything else is invalid!
    df.loc[~df["loan_status"].isin([0, 1]), "loan_status"] = np.nan
    df["loan_status"] = pd.to_numeric(df["loan_status"], errors="coerce")

    # default_flag is just a friendly copy of loan_status (1 = defaulted, 0 = paid)
    df["default_flag"] = df["loan_status"]

    # -------------------------------------------------------------------------
    # STEP 6: Group numbers into simple, human-friendly buckets (Banding)
    # -------------------------------------------------------------------------
    # Instead of looking at exact dollar amounts, let's put people into easy buckets:
    # E.g., Low Income (<=25k), Medium (25k-50k), High (100k-200k), Super High (>200k)
    df["income_band"] = pd.cut(
        df["person_income"],
        bins=[-np.inf, 25000, 50000, 100000, 200000, np.inf],
        labels=["<=25k", "25k-50k", "50k-100k", "100k-200k", ">200k"]
    )

    # Do the same bucketing for loan amount: Tiny (<=5k), Medium (10k-20k), Large (>35k)
    df["loan_amount_band"] = pd.cut(
        df["loan_amnt"],
        bins=[-np.inf, 5000, 10000, 20000, 35000, np.inf],
        labels=["<=5k", "5k-10k", "10k-20k", "20k-35k", ">35k"]
    )

    # Save our nice, tidy cleaned dataset
    df.to_csv(out / "credit_risk_clean.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 7: Calculate Overall High-Level KPIs (Key Performance Indicators)
    # -------------------------------------------------------------------------
    # We only want to analyze rows where we actually know whether the loan defaulted or not
    valid = df.dropna(subset=["loan_status"]).copy()

    # Big picture numbers:
    # - default_rate_pct: Out of 100 people, how many failed to pay back?
    # - average_loan_amount: What was the average size of a loan?
    # - median_loan_amount: The middle loan size if everyone lined up smallest to largest
    overall = pd.DataFrame([{
        "source_rows": original_rows,
        "rows_after_deduplication": len(df),
        "labeled_rows": len(valid),
        "duplicate_rows_removed": original_rows - len(df),
        "default_rate_pct": round(float(valid["loan_status"].mean() * 100), 2) if len(valid) else np.nan,
        "average_loan_amount": round(float(valid["loan_amnt"].mean()), 2) if len(valid) else np.nan,
        "median_loan_amount": round(float(valid["loan_amnt"].median()), 2) if len(valid) else np.nan,
        "average_interest_rate_pct": round(float(valid["loan_int_rate"].mean()), 2) if len(valid) else np.nan,
        "missing_loan_status_rows": int(df["loan_status"].isna().sum()),
    }])
    overall.to_csv(out / "overall_kpis.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 8: Breakdown stats by different categories (Slicing & Dicing)
    # -------------------------------------------------------------------------
    # We want to see default rates across 5 different categories:
    # 1. By Grade (Are 'A' borrowers really safer than 'G' borrowers?)
    # 2. By Intent (Do education loans default less than personal loans?)
    # 3. By Home Ownership (Do homeowners default less than renters?)
    # 4. By Income Band (Do richer people pay back more reliably?)
    # 5. By Loan Amount Band (Are huge loans riskier?)
    group_specs = {
        "default_by_grade.csv": "loan_grade",
        "default_by_intent.csv": "loan_intent",
        "default_by_home_ownership.csv": "person_home_ownership",
        "default_by_income_band.csv": "income_band",
        "default_by_loan_amount_band.csv": "loan_amount_band",
    }

    for filename, col in group_specs.items():
        # Group by the category and calculate total applications, defaults, and percentages
        table = valid.groupby(col, dropna=False, observed=False).agg(
            applications=("loan_status", "size"),
            defaults=("loan_status", "sum"),
            default_rate_pct=("loan_status", lambda s: round(float(s.mean() * 100), 2)),
            avg_loan_amount=("loan_amnt", "mean"),
            avg_interest_rate_pct=("loan_int_rate", "mean")
        ).reset_index()
        # Save each breakdown table to its own CSV file
        table.to_csv(out / filename, index=False)

    # -------------------------------------------------------------------------
    # STEP 9: Print friendly success message to terminal
    # -------------------------------------------------------------------------
    print(f"Validated input: {args.input}")
    print(f"Rows read: {original_rows}; rows after deduplication: {len(df)}; labeled rows: {len(valid)}")
    print("Wrote data-quality report, cleaned data and KPI segment tables to:", out.resolve())
    print("Computed metrics are based on this run's input file; review data_quality.csv before interpreting results.")


if __name__ == "__main__":
    main()
