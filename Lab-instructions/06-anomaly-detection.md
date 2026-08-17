# 06 · Anomaly Detection — *Finding outliers with z-scores*

Use Case #2. Flag transactions whose revenue is unusually far from the average.

---

## Objective

Compute a z-score for each transaction's revenue and flag the ones beyond a chosen
standard-deviation threshold as anomalies.

## Key concepts

- **z-score** = `(value − mean) / stddev`. It re-expresses a value as "how many standard
  deviations from the mean," which makes a threshold comparable across scales.
- A common rule: `|z| > 2` (~beyond 2σ) is anomalous. The threshold is a **knob** — tighter
  (1.5σ) flags more, looser (3σ) flags fewer.
- Choose your baseline deliberately: z-score against the **whole dataset**, or against each
  **category** separately (a $900 electronics sale is normal; a $900 food sale is not).

## Steps

1. **Global stats.** Compute `F.mean("revenue")` and `F.stddev("revenue")` over the full
   dataset (a single-row aggregate you then broadcast/cross-join back, or compute over an
   unbounded window).
2. **z-score column.** Add `z = (revenue − mean) / stddev`.
3. **Flag anomalies.** Add `is_anomaly = F.abs(z) > THRESHOLD` with `THRESHOLD = 2.0` as a
   named constant. List the flagged rows with customer, category, revenue, and z.
4. **Per-category variant.** Repeat using a `Window.partitionBy("category")` for the mean and
   stddev so each transaction is judged against its own category. Compare which anomalies
   appear globally vs per-category.
5. **Tunable threshold.** Because `THRESHOLD` is a constant, re-running at 1.5σ (Exercise 6)
   is a one-line change — note how the flagged count grows.

> **Small-sample caveat:** with only 20 rows, `stddev` is volatile and a single big sale
> pulls the mean. Treat this as a *mechanics* exercise; real anomaly detection needs far more
> data and often a robust statistic (median/MAD) instead of mean/stddev.
> Also decide up front: **sample** vs **population** stddev (`stddev`/`stddev_samp` vs
> `stddev_pop`) — they differ noticeably at n = 20.

## Expected output

- Every transaction annotated with `z` and `is_anomaly`.
- A short list of flagged transactions — at 2σ globally, expect roughly the one or two
  largest electronics sales to surface.
- A per-category list that flags different rows than the global version.

## Checkpoint

- Which transaction has the **largest** absolute z-score globally?
- Does the per-category baseline flag anything the global one misses (or vice versa)? Why?
- How does the flag count change going from 2σ → 1.5σ, and what does that say about
  threshold choice?

---

[← 05 · Segmentation](Lab-instructions/05-customer-segmentation.md) · [Index](Lab-instructions/index.md) · [Next: 07 · Data Engineering →](Lab-instructions/07-data-engineering-parquet.md)
