# 08 · Hands-On Exercises

Extend the lab yourself. Each exercise names the goal, the technique to reach for, and how
to know you got it right — no solution code, on purpose.

---

### 1. Descriptive — most expensive category per region
- **Goal:** Add a `revenue_per_unit` column, then find the most expensive category in each region.
- **Reach for:** `unit_price` (or `revenue / quantity`), then a window `partitionBy("region").orderBy(desc("revenue_per_unit"))` with a rank filtered to 1.
- **Done when:** you have exactly one top category per region.

### 2. Diagnostic — credit_card vs cash average revenue
- **Goal:** Filter to `credit_card` transactions and compare their average revenue against `cash`.
- **Reach for:** `filter` + `groupBy("payment_method").agg(F.avg("revenue"))`, or an `isin(["credit_card","cash"])` filter then group.
- **Done when:** you can state which method has the higher average — and whether the gap is meaningful at this sample size.

### 3. Window — previous purchase per customer
- **Goal:** Add `prev_transaction_revenue` showing each customer's prior purchase amount.
- **Reach for:** `F.lag("revenue").over(Window.partitionBy("customer").orderBy("event_time"))`.
- **Done when:** each customer's earliest row is `null` and later rows carry the prior value.

### 4. Feature engineering — does high quantity track payment method?
- **Goal:** Add a `high_quantity` flag (`quantity > 3`) and check whether it correlates with payment method.
- **Reach for:** the flag via `F.when`, then a `groupBy("payment_method", "high_quantity").count()` crosstab (or `stat.crosstab`).
- **Done when:** you can describe any lean (e.g. bulk buys skewing toward cash) and note the small-sample caveat.

### 5. Segmentation — retune the RFM thresholds
- **Goal:** Adjust the Part 5 scoring/segment thresholds and observe how segment sizes change.
- **Reach for:** the named threshold constants; change one, re-run the segment counts.
- **Done when:** you can show a before/after of segment sizes and explain the shift.

### 6. Anomaly detection — tighten to 1.5σ
- **Goal:** Change the threshold from 2σ to 1.5σ and count the additional anomalies.
- **Reach for:** the `THRESHOLD` constant from Part 6.
- **Done when:** you report how many *more* rows are flagged and which new ones appear.

### 7. Challenge — `region_health_score`
- **Goal:** Build a single composite score per region combining **total revenue**, **average order value**, and **transaction count**.
- **Reach for:** compute the three metrics per region, **normalize** each to a common scale
  (min–max or z-score across regions — raw dollars and counts aren't comparable), then take a
  weighted sum. Decide and justify your weights.
- **Done when:** every region has one comparable score and you can defend why the ranking makes sense.

---

[← 07 · Data Engineering](07-data-engineering-parquet.md) · [Index](index.md)
