-- ==============================================================================
-- BABY EXPLANATION:
-- SQL is like asking questions to a giant digital librarian!
-- "SELECT" means "Show me these answers".
-- "FROM" means "Look inside this table".
-- "WHERE" means "Only look at rows matching this rule".
-- "GROUP BY" means "Sort into piles by category (like sorting Lego bricks by colour)".
-- ==============================================================================


-- ------------------------------------------------------------------------------
-- QUESTION 1: What are our big overall numbers?
-- Let's find:
-- - How many total people did we look at? (COUNT(*))
-- - How many failed to pay back? (SUM(loan_status))
-- - What percentage failed? (AVG(loan_status) * 100)
-- - What was the average loan size and average interest rate?
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(*) AS labeled_applications,                    -- Total people counted
    SUM(loan_status) AS defaults,                         -- Count of people who defaulted
    ROUND(100.0 * AVG(loan_status), 2) AS default_rate_pct, -- What % defaulted (e.g. 21.87%)
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,          -- Average loan in $
    ROUND(AVG(loan_int_rate), 2) AS avg_interest_rate_pct -- Average interest %
FROM credit_risk 
WHERE loan_status IN (0, 1);                              -- Only look at rows with a clear 0 or 1


-- ------------------------------------------------------------------------------
-- QUESTION 2: How risky is each loan grade (A, B, C, D, E, F, G)?
-- We sort people into grade piles and see which grades default the most.
-- (Spoiler: A is the safest, G is the most dangerous!)
-- ------------------------------------------------------------------------------
SELECT 
    loan_grade,                                           -- The risk letter (A, B, C...)
    COUNT(*) AS applications,                             -- How many people had this grade
    SUM(loan_status) AS defaults,                         -- How many of them failed to pay
    ROUND(100.0 * AVG(loan_status), 2) AS default_rate_pct, -- Percentage who failed to pay
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount           -- Average loan size for this grade
FROM credit_risk 
WHERE loan_status IN (0, 1)
GROUP BY loan_grade                                       -- Pile them by grade
ORDER BY default_rate_pct DESC;                           -- Show highest risk first!


-- ------------------------------------------------------------------------------
-- QUESTION 3: Why did people borrow money, and did some reasons default more?
-- (e.g., Medical emergencies vs Education vs Debt Consolidation)
-- ------------------------------------------------------------------------------
SELECT 
    loan_intent,                                          -- The reason: EDUCATION, MEDICAL, etc.
    COUNT(*) AS applications,                             -- How many people asked for this reason
    SUM(loan_status) AS defaults,                         -- How many failed to pay
    ROUND(100.0 * AVG(loan_status), 2) AS default_rate_pct  -- What % failed to pay
FROM credit_risk 
WHERE loan_status IN (0, 1)
GROUP BY loan_intent                                      -- Pile them by reason
ORDER BY default_rate_pct DESC;                           -- Show highest risk reason first!


-- ------------------------------------------------------------------------------
-- QUESTION 4: Loan-to-income burden (How heavy is the loan compared to their paycheck?)
-- If someone borrows more than 30% of their yearly salary, do they fail more often?
-- We use "CASE WHEN" (like an IF-THEN statement) to create simple burden baskets:
--   <10%, 10-20%, 20-30%, or 30%+
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN loan_percent_income < 0.10 THEN '<10%'
        WHEN loan_percent_income < 0.20 THEN '10-20%'
        WHEN loan_percent_income < 0.30 THEN '20-30%' 
        ELSE '30%+' 
    END AS burden_band,                                   -- Which burden basket they fall into
    COUNT(*) AS applications,                             -- Total applicants in this basket
    ROUND(100.0 * AVG(loan_status), 2) AS default_rate_pct  -- Default rate in this basket
FROM credit_risk 
WHERE loan_status IN (0, 1) 
  AND loan_percent_income >= 0                            -- Ignore silly negative numbers
GROUP BY burden_band
ORDER BY burden_band;


-- ------------------------------------------------------------------------------
-- QUESTION 5: Give a leaderboard ranking (1st, 2nd, 3rd) to grades by default risk!
-- "WITH ... AS" is like making a temporary scratchpad note.
-- "DENSE_RANK() OVER (...)" ranks items 1, 2, 3 without skipping numbers.
-- ------------------------------------------------------------------------------
WITH grade_kpis AS (
    -- Scratchpad note: Calculate default rate for each grade first
    SELECT 
        loan_grade, 
        COUNT(*) AS applications, 
        AVG(loan_status) AS default_rate
    FROM credit_risk 
    WHERE loan_status IN (0, 1) 
    GROUP BY loan_grade
)
SELECT 
    loan_grade,                                           -- Grade letter (A to G)
    applications,                                         -- Total applicants
    ROUND(default_rate * 100, 2) AS default_rate_pct,     -- Default percentage
    DENSE_RANK() OVER (ORDER BY default_rate DESC) AS risk_rate_rank -- Rank: #1 is highest risk!
FROM grade_kpis 
ORDER BY risk_rate_rank, loan_grade;
