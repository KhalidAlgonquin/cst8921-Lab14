# 02 · Diagnostic Analytics — *Why did it happen?*

Drill from the headline numbers into the cross-sections and trends behind them.

---

## Objective

Move past single-dimension totals into two-dimensional views and time trends, so you can
explain *why* a region or category looks the way it does.

## Key concepts

- **Diagnostic analytics** looks for the drivers behind a result — usually by slicing along
  a second dimension or across time.
- **Pivot** turns distinct values of a column into columns of their own (a crosstab).
- **Time bucketing** groups timestamps into months/weeks/days for trend lines.

## Steps

1. **Region × Category pivot.** `groupBy("region").pivot("category").agg(F.sum("revenue"))`
   to get a region-by-category revenue matrix. This is the single most useful diagnostic
   view here — it shows which category drives each region.
2. **Drill-down.** Pick the top region from Part 1, `filter` to it, and list its
   transactions ordered by revenue. Confirm the pivot's story at the row level.
3. **Monthly trend.** Derive a month bucket from `event_time` (use `F.date_format(..., "yyyy-MM")`
   or `F.month`), then `groupBy` it and sum revenue. Order chronologically to see the
   Jan → Mar movement.
4. **Two-factor trend (optional).** `groupBy` month **and** category to see whether a
   category's share shifts over the quarter.
5. **Payment-method cut.** `groupBy("payment_method")` with average revenue — sets up
   Exercise 2 later.

> **Watch the null cells** in a pivot: a region/category combination that never occurred
> shows as `null`, not `0`. Decide deliberately whether to `fillna(0)` — it changes any
> average you compute on top.

## Expected output

- A pivot table: rows = regions, columns = Electronics / Clothing / Food, cells = summed
  revenue (some `null`).
- A single-region drill-down list.
- A 3-row monthly trend (2024-01, 2024-02, 2024-03) showing how quarterly revenue moves.

## Checkpoint

- In the pivot, which single category is carrying each region?
- Is the monthly trend rising, falling, or flat — and is that a real signal or an artifact
  of only 20 rows?
- Why might `AVG(revenue)` by payment method mislead on a dataset this small?

---

[← 01 · Descriptive](01-descriptive-analytics.md) · [Index](index.md) · [Next: 03 · Window Functions →](03-window-functions.md)
