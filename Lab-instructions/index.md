# Big Data Analytics Lab — Instructor & Learner Guide
### Optimize Business Processes Using Big Data Analytics with PySpark

This lab walks through the full spectrum of big data analytics on a simulated retail
transactions dataset. Each part is a self-contained instruction file: read the objective,
follow the numbered steps, check your output against the expected result, then move on
using the navigation links at the bottom of each page.

> **How to use these files:** These are *instructions to navigate the lab* — they tell you
> what to build and which PySpark techniques to reach for at each step. You write the code.
> Start at **[Setup](00-setup.md)**, then work through Parts 1–7 in order. Part 8 is optional
> practice.

---

## Lab Map

| Part | File | Topic | Analytics type |
|------|------|-------|----------------|
| — | [00 · Setup](00-setup.md) | Environment, dataset, schema, derived columns | Foundation |
| 1 | [01 · Descriptive](01-descriptive-analytics.md) | Summary stats, revenue by category/region | Descriptive |
| 2 | [02 · Diagnostic](02-diagnostic-analytics.md) | Drill-down, pivot, monthly trends | Diagnostic |
| 3 | [03 · Window Functions](03-window-functions.md) | Rankings, running totals, `partitionBy` | Advanced |
| 4 | [04 · Feature Engineering](04-predictive-feature-engineering.md) | RFM scoring, ML feature engineering | Predictive |
| 5 | [05 · Segmentation](05-customer-segmentation.md) | Customer segments (Champions → At Risk) | Use case |
| 6 | [06 · Anomaly Detection](06-anomaly-detection.md) | Outliers via z-scores | Use case |
| 7 | [07 · Data Engineering](07-data-engineering-parquet.md) | Parquet output for downstream use | Data engineering |
| 8 | [08 · Hands-On Exercises](08-hands-on-exercises.md) | Extend the lab yourself | Practice |

---

## What you'll practice

- **Aggregations** — `groupBy`, `agg`, `pivot`, `describe`
- **Window functions** — `rank()`, `dense_rank()`, `row_number()`, `ntile()`, running totals, `lag()`, `partitionBy`
- **Feature engineering** — hour/day/month extraction, RFM scoring, binary flags
- **Statistical methods** — mean, standard deviation, z-score thresholds
- **Spark SQL** — the DataFrame-API equivalents of common SQL patterns
- **Storage** — writing partitioned Parquet for downstream analytics

## Tools

- PySpark DataFrame API (distributed processing)
- Spark SQL functions (`F.col`, `F.when`, `F.window`, `F.ntile`, …)
- Parquet columnar storage

---

## Learning flow

Each part page follows the same shape so you always know where you are:

1. **Objective** — the business question this part answers
2. **Key concepts** — the ideas you need before you start
3. **Steps** — numbered instructions naming the operations/functions to apply
4. **Expected output** — what your result should look like (shape, not values to copy)
5. **Checkpoint** — questions to confirm you understood it

➡️ **Begin here:** [00 · Setup](Lab-instructions/00-setup.md)
