-- ==============================================================================
-- BABY EXPLANATION:
-- What is a table? Imagine creating a brand-new notebook with labelled columns!
-- Each column only accepts a certain kind of data:
--   INTEGER: whole numbers (like 1, 2, 25)
--   REAL: numbers with decimal points (like $10.50 or 7.25%)
--   TEXT: words and letters (like "RENT", "OWN", "EDUCATION")
-- ==============================================================================

-- Create our table named 'credit_risk' if it doesn't already exist.
-- You can load 'credit_risk_clean.csv' directly into this table.
CREATE TABLE IF NOT EXISTS credit_risk (
    person_age                  INTEGER, -- Age of the person in years (e.g., 25)
    person_income               REAL,    -- Yearly income in dollars (e.g., 50000.0)
    person_home_ownership       TEXT,    -- House status: "RENT", "OWN", or "MORTGAGE"
    person_emp_length           REAL,    -- How many years they have worked at their job
    loan_intent                 TEXT,    -- Reason for loan: "EDUCATION", "MEDICAL", etc.
    loan_grade                  TEXT,    -- Bank risk letter: "A" (safest) through "G" (riskiest)
    loan_amnt                   REAL,    -- Borrowed money in dollars (e.g., 10000.0)
    loan_int_rate               REAL,    -- Interest fee percentage (e.g., 11.2%)
    loan_status                 INTEGER, -- Did they pay? 0 = Yes (Good!), 1 = Defaulted (Bad!)
    loan_percent_income         REAL,    -- Loan amount divided by income (burden ratio)
    cb_person_default_on_file   TEXT,    -- Have they broken a promise before? ("Y" or "N")
    cb_person_cred_hist_length  REAL,    -- Years since opening their very first credit card
    default_flag                INTEGER, -- Same as loan_status: 1 = defaulted, 0 = paid
    income_band                 TEXT,    -- Income bucket: e.g. "<=25k", "25k-50k", ">200k"
    loan_amount_band            TEXT     -- Loan bucket: e.g. "<=5k", "5k-10k", ">35k"
);

-- ==============================================================================
-- What is an INDEX?
-- Think of an index like bookmarks or the index at the back of a textbook!
-- It helps the database find answers super fast instead of reading every page.
-- ==============================================================================

-- Create an index on 'loan_grade' so questions about grades (A, B, C...) run lightning fast
CREATE INDEX IF NOT EXISTS idx_credit_grade ON credit_risk(loan_grade);

-- Create an index on 'loan_intent' so questions about reasons (Medical, Education...) run lightning fast
CREATE INDEX IF NOT EXISTS idx_credit_intent ON credit_risk(loan_intent);
