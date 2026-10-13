# Power BI Dashboard Specification — Credit Risk Analytics

This specification details the exact canvas layout, visual objects, fields, and formatting rules to reproduce the dashboard shown in `powerbi/dashboard_preview.png`.

---

## 1. Canvas Setup & Theme
* **Canvas Size:** 16:9 widescreen (1920 × 1080 px or standard 1280 × 720 px)
* **Background:** Light grey/off-white (`#F4F6F9`)
* **Color Palette:**
  * **Primary Navy:** `#0F2C59` (Main bar fills and headers)
  * **Accent Blue:** `#3B82F6` (Line chart trend)
  * **Alert / Risk Red:** `#EF4444` (High default highlights)
  * **Cards Background:** Pure white (`#FFFFFF`) with subtle soft shadow

---

## 2. Top Header & Slicer Bar
Place at the top of the canvas (`Y: 10px`, `Height: 80px`):
* **Title TextBox:** "Credit Risk & Loan Default Portfolio Analytics" (Font: Segoe UI Semibold, 22pt, Navy)
* **Dropdown Slicers:**
  1. `credit_risk[loan_grade]` — Slicer header: "Loan Grade" (Selection: All, Multi-select enabled)
  2. `credit_risk[loan_intent]` — Slicer header: "Loan Purpose" (Selection: All)
  3. `credit_risk[person_home_ownership]` — Slicer header: "Home Ownership" (Selection: All)
  4. `credit_risk[income_band]` — Slicer header: "Income Band" (Selection: All)

---

## 3. KPI Summary Cards (Row 1)
5 single-value Card visuals placed horizontally across the canvas:

| Card Title | DAX Measure | Target Format | Displayed Value (All Data) |
| :--- | :--- | :--- | :--- |
| **Labeled Applications** | `[Labeled Applications]` | Whole Number (`#,##0`) | `32,416` |
| **Total Defaults** | `[Total Defaults]` | Whole Number (`#,##0`) | `7,090` |
| **Default Rate** | `[Default Rate %]` | Percentage (`0.00%` or `0.0%`) | `21.87%` |
| **Average Loan Amount** | `[Average Loan Amount]` | Currency (`$#,##0`) | `$9,594` |
| **Average Interest Rate** | `[Average Interest Rate %]` | Percentage (`0.00%`) | `11.02%` |

---

## 4. Visual 1: Application Count & Default Rate by Loan Grade (Combo Chart)
* **Visual Type:** Line and Clustered Column Chart
* **Position:** Left quadrant (`Width: 50%`, `Height: 420px`)
* **X-Axis:** `credit_risk[loan_grade]` (Sorted ascending: A, B, C, D, E, F, G)
* **Column Values (Y-Axis):** `[Applications]` (Bar Color: Navy `#0F2C59`)
* **Line Values (Secondary Y-Axis):** `[Default Rate %]` (Line Color: Blue `#3B82F6`, Stroke: 3px)
* **Data Labels:** Turned On for both column and line
* **Key Visual Pattern:** Shows loan volume concentrated in Grades A & B (~10k each), while default rate climbs steeply from **9.96%** in Grade A to **98.44%** in Grade G.

---

## 5. Visual 2: Default Rate by Loan Purpose (Horizontal Bar Chart)
* **Visual Type:** Clustered Bar Chart
* **Position:** Top-Right quadrant (`Width: 48%`, `Height: 250px`)
* **Y-Axis:** `credit_risk[loan_intent]` (Sorted descending by Default Rate)
* **X-Axis:** `[Default Rate %]` (Data Labels: On, 1 decimal place)
* **Bar Fills:** Navy `#0F2C59`
* **Rankings Shown:**
  1. Debt Consolidation: `28.7%`
  2. Medical: `26.8%`
  3. Home Improvement: `26.2%`
  4. Personal: `19.9%`
  5. Education: `17.3%`
  6. Venture: `14.9%`

---

## 6. Visual 3: Home Ownership Distribution (Donut Chart)
* **Visual Type:** Donut Chart
* **Position:** Bottom-Center quadrant
* **Legend:** `credit_risk[person_home_ownership]` ("RENT", "MORTGAGE", "OWN", "OTHER")
* **Values:** `[Applications]`
* **Data Labels:** Category & Percentage of Total
* **Insights:** Renters form the largest applicant block, followed by Mortgage and Homeowners.

---

## 7. Visual 4: Segment Performance Matrix (Table / Matrix)
* **Visual Type:** Matrix
* **Position:** Bottom-Right quadrant
* **Rows:** `credit_risk[person_home_ownership]`
* **Values:**
  * `[Applications]`
  * `[Total Defaults]`
  * `[Default Rate %]`
  * `[Average Loan Amount]`
* **Style:** Alternating rows, bold subtotals, conditional background data bars on Default Rate.

---

## 8. Data Model & Relationships
* **Table:** `credit_risk` (Import from `data/processed/credit_risk_clean.csv`)
* Ensure column data types:
  * `loan_status` & `default_flag`: Whole Number (0 or 1)
  * `loan_amnt`, `person_income`: Decimal / Currency
  * `loan_int_rate`, `loan_percent_income`: Decimal Number
