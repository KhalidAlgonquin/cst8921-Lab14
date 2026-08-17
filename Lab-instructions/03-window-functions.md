# 03 · Window Functions — *Rankings & running totals*

The advanced core of the lab: compute per-row values that depend on a *window* of related
rows, without collapsing the DataFrame the way `groupBy` does.

---

## Objective

Rank transactions within their region, build running totals over time, split rows into
quartiles, and reach back to a previous row — all with window functions.

## Key concepts

- A **window** is defined by `Window.partitionBy(...).orderBy(...)` and an optional **frame**.
- `partitionBy` = the group each row is ranked *within*; `orderBy` = the order inside it.
- **Ranking family:** `row_number()` (unique, no ties), `rank()` (ties share a rank, leaves
  gaps), `dense_rank()` (ties share a rank, no gaps).
- **`ntile(n)`** splits each partition into `n` roughly equal buckets — the basis for RFM
  scoring in Part 4.
- **Frames** control which rows the function sees:
  - `rowsBetween(Window.unboundedPreceding, Window.currentRow)` → **running total**.
  - Default frame differs for ranking vs aggregate functions — always set it explicitly for
    running totals so results are deterministic.
- **`lag()` / `lead()`** pull a value from a previous/next row in the ordered window.

## Steps

1. **Rank within region.** Define a window `partitionBy("region").orderBy(F.desc("revenue"))`
   and add a rank column with `F.rank()` (or `dense_rank()`). Each region restarts at 1.
2. **Top-N per region.** Filter the ranked result to rank ≤ 2 to get each region's top
   transactions.
3. **Running total over time.** Window `partitionBy("region").orderBy("event_time")` with an
   explicit `rowsBetween(unboundedPreceding, currentRow)` frame; apply `F.sum("revenue").over(w)`
   for a cumulative revenue curve per region.
4. **Quartiles.** Add `F.ntile(4).over(...)` over revenue to bucket transactions into 4 value
   tiers — note how bucket sizes fall out when the row count isn't divisible by 4.
5. **Previous purchase.** Window `partitionBy("customer").orderBy("event_time")`; use
   `F.lag("revenue").over(w)` to attach each customer's previous transaction revenue (feeds
   Exercise 3).

> **`rowsBetween` vs `rangeBetween`:** `rowsBetween` counts physical rows; `rangeBetween`
> counts by the *value* of the `orderBy` key (e.g. all rows within N days). For a plain
> running total, `rowsBetween` is what you want.

## Expected output

- A ranked table where the rank column resets to 1 at each region boundary.
- A running-total column that only ever increases within a region and resets across regions.
- An `ntile` column with values 1–4.
- A `prev_revenue` column that is `null` for each customer's first (earliest) transaction.

## Checkpoint

- When would `rank()` and `dense_rank()` give different numbers here — and does this data
  actually contain a tie?
- Why does the running total need an explicit frame while `rank()` does not?
- What does a `null` in the `lag` column tell you about that row?

---

[← 02 · Diagnostic]Lab-instructions/(02-diagnostic-analytics.md) · [Index](Lab-instructions/index.md) · [Next: 04 · Feature Engineering →](Lab-instructions/04-predictive-feature-engineering.md)
