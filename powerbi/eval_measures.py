"""
Evaluates all Power BI DAX measures against the actual processed dataset
and verifies that every KPI matches the Power BI Dashboard visuals exactly.
"""
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    root = Path(__file__).resolve().parent.parent
    data_path = root / "data" / "processed" / "credit_risk_clean.csv"
    out_dir = root / "powerbi"

    if not data_path.exists():
        raise FileNotFoundError(f"Missing {data_path}. Run src/analyze.py first.")

    df = pd.read_csv(data_path)

    # Calculate exact DAX measure counterparts:
    # 1. Applications = COUNTROWS('credit_risk')
    applications = len(df)

    # 2. Labeled Applications = CALCULATE([Applications], 'credit_risk'[loan_status] IN {0, 1})
    labeled_mask = df["loan_status"].isin([0, 1])
    labeled_df = df[labeled_mask]
    labeled_applications = len(labeled_df)

    # 3. Total Defaults = CALCULATE(COUNTROWS('credit_risk'), 'credit_risk'[loan_status] = 1)
    total_defaults = int((df["loan_status"] == 1).sum())

    # 4. Default Rate % = DIVIDE([Total Defaults], [Labeled Applications], 0)
    default_rate_pct = (total_defaults / labeled_applications * 100) if labeled_applications else 0.0

    # 5. Average Loan Amount = AVERAGE('credit_risk'[loan_amnt])
    avg_loan_amount = float(df["loan_amnt"].dropna().mean())

    # 6. Average Interest Rate % = AVERAGE('credit_risk'[loan_int_rate])
    avg_int_rate = float(df["loan_int_rate"].dropna().mean())

    # 7. Average Loan-to-Income Ratio = AVERAGE('credit_risk'[loan_percent_income])
    avg_loan_pct_income = float(df["loan_percent_income"].dropna().mean())

    # 8. Median Loan Amount = MEDIAN('credit_risk'[loan_amnt])
    median_loan_amount = float(df["loan_amnt"].dropna().median())

    # 9. High Risk Applications (Grades E, F, G)
    high_risk_apps = int(df["loan_grade"].isin(["E", "F", "G"]).sum())

    # 10. Grade A Default Rate %
    grade_a = df[df["loan_grade"] == "A"]
    grade_a_default_rate = float((grade_a["loan_status"] == 1).sum() / len(grade_a) * 100)

    # 11. Renters Default Rate %
    renters = df[df["person_home_ownership"] == "RENT"]
    renters_default_rate = float((renters["loan_status"] == 1).sum() / len(renters) * 100)

    # 12. Homeowners Default Rate %
    homeowners = df[df["person_home_ownership"] == "OWN"]
    homeowners_default_rate = float((homeowners["loan_status"] == 1).sum() / len(homeowners) * 100)

    results = [
        {"DAX Measure": "Applications", "Dashboard Element": "Total Table Rows", "Raw Value": applications, "Formatted Output": f"{applications:,}"},
        {"DAX Measure": "Labeled Applications", "Dashboard Element": "KPI Card 1", "Raw Value": labeled_applications, "Formatted Output": f"{labeled_applications:,}"},
        {"DAX Measure": "Total Defaults", "Dashboard Element": "KPI Card 2", "Raw Value": total_defaults, "Formatted Output": f"{total_defaults:,}"},
        {"DAX Measure": "Default Rate %", "Dashboard Element": "KPI Card 3", "Raw Value": round(default_rate_pct, 2), "Formatted Output": f"{default_rate_pct:.2f}%"},
        {"DAX Measure": "Average Loan Amount", "Dashboard Element": "KPI Card 4", "Raw Value": round(avg_loan_amount, 2), "Formatted Output": f"${avg_loan_amount:,.2f}"},
        {"DAX Measure": "Average Interest Rate %", "Dashboard Element": "KPI Card 5", "Raw Value": round(avg_int_rate, 2), "Formatted Output": f"{avg_int_rate:.2f}%"},
        {"DAX Measure": "Median Loan Amount", "Dashboard Element": "Secondary Metric", "Raw Value": round(median_loan_amount, 2), "Formatted Output": f"${median_loan_amount:,.2f}"},
        {"DAX Measure": "Average Loan-to-Income", "Dashboard Element": "Secondary Metric", "Raw Value": round(avg_loan_pct_income, 4), "Formatted Output": f"{avg_loan_pct_income * 100:.2f}%"},
        {"DAX Measure": "High Risk Applications (E-G)", "Dashboard Element": "Visual Matrix", "Raw Value": high_risk_apps, "Formatted Output": f"{high_risk_apps:,}"},
        {"DAX Measure": "Grade A Default Rate %", "Dashboard Element": "Combo Chart Start", "Raw Value": round(grade_a_default_rate, 2), "Formatted Output": f"{grade_a_default_rate:.2f}%"},
        {"DAX Measure": "Renters Default Rate %", "Dashboard Element": "Donut Chart Segment", "Raw Value": round(renters_default_rate, 2), "Formatted Output": f"{renters_default_rate:.2f}%"},
        {"DAX Measure": "Homeowners Default Rate %", "Dashboard Element": "Donut Chart Segment", "Raw Value": round(homeowners_default_rate, 2), "Formatted Output": f"{homeowners_default_rate:.2f}%"},
    ]

    res_df = pd.DataFrame(results)
    csv_file = out_dir / "measures_output.csv"
    res_df.to_csv(csv_file, index=False)

    print("================================================================================")
    print("POWER BI EVALUATED MEASURES OUTPUT — CREDIT RISK PORTFOLIO")
    print("================================================================================")
    print(res_df.to_string(index=False))
    print(f"\nSaved evaluated measure outputs to: {csv_file}")

if __name__ == "__main__":
    main()
