# 04 · Feature Engineering — *Preparing for prediction*

Turn raw transactions into model-ready features, and compute the RFM scores that Part 5
segments on.

---

## Objective

Engineer time features and binary flags at the transaction level, then aggregate to
customer-level **Recency / Frequency / Monetary** features and score each into tiers.

## Key concepts

- **Feature engineering** = deriving signal-bearing columns a model can learn from.
- **RFM** is a classic customer-value framework:
  - **Recency** — how long since the customer's last purchase (lower = better)
  - **Frequency** — how many purchases (higher = better)
  - **Monetary** — total spend (higher = better)
- **Scoring** maps each raw RFM value into a small ordinal tier (here 1–4) with `ntile`, so
  they're comparable and combinable.

## Steps

### A. Transaction-level features

1. **Time parts.** From `event_time`, extract `F.hour`, `F.dayofmonth`, `F.dayofweek`,
   and `F.month` into their own columns.
2. **Binary flags** with `F.when(...).otherwise(...)` cast to int:
   - `is_weekend` — `dayofweek` in {1, 7} (Spark: 1 = Sunday, 7 = Saturday)
   - `is_high_value` — `revenue` above some threshold (e.g. the dataset mean)
   - `high_quantity` — `quantity > 3` (feeds Exercise 4)

### B. Customer-level RFM

3. **Reference date.** Pick a snapshot date — the simplest choice is
   `max(event_time)` across the data (optionally + 1 day) so the most recent buyer has the
   smallest non-zero recency.
4. **Aggregate per customer** with `groupBy("customer")`:
   - `recency_days` = `F.datediff(reference_date, F.max("event_time"))`
   - `frequency` = `F.count("*")`
   - `monetary` = `F.sum("revenue")`
5. **Score into tiers (1–4)** using `ntile(4)` over each metric — mind the direction:
   - **Recency:** order **ascending** (smaller days = more recent), then invert so recent
     buyers get the **high** score (e.g. `R = 5 - ntile`). Decide your convention and keep
     it consistent.
   - **Frequency / Monetary:** order ascending, `ntile` directly (higher value → higher tier).
6. **Combine.** Add `rfm_sum = R + F + M` (range 3–12) and/or a concatenated `rfm_cell`
   like `"R4F3M4"`. These are the inputs Part 5 turns into named segments.

> **Direction is the classic bug.** A customer who bought yesterday should get a *high* R
> score, not a low one. Write a one-line assertion or eyeball the most-recent buyer to
> confirm your inversion is right before moving on.

## Expected output

- The transaction DataFrame widened with `hour / day / dayofweek / month` and the three
  0/1 flag columns.
- A customer-level table (9 rows) with `recency_days`, `frequency`, `monetary`, their `R/F/M`
  tiers, and `rfm_sum`.

## Checkpoint

- With 9 customers and `ntile(4)`, how many customers land in each tier — and why aren't the
  buckets exactly equal?
- Why must Recency be scored in the opposite direction from Frequency and Monetary?
- Which single customer looks most valuable on `rfm_sum`? Does that match intuition from the
  raw data?

---

[← 03 · Window Functions](Lab-instructions/03-window-functions.md) · [Index](Lab-instructions/index.md) · [Next: 05 · Segmentation →](Lab-instructions/05-customer-segmentation.md)
