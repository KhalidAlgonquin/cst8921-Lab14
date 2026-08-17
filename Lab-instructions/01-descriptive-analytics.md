# 01 · Descriptive Analytics — *What happened?*

Summarize the dataset and roll revenue up by category and region.

---

## Objective

Produce the headline numbers a business would look at first: overall stats, and where the
money comes from (which categories, which regions).

## Key concepts

- **Descriptive analytics** answers *what happened* — no causes, no predictions, just facts.
- **Aggregation** collapses many rows into summary rows with `groupBy` + `agg`.
- `describe()` gives count / mean / stddev / min / max for numeric columns in one shot.

## Steps

1. **Summary statistics.** Call `describe()` on the numeric columns (`unit_price`,
   `quantity`, `revenue`) to get count, mean, stddev, min, max. Read it as a sanity check —
   do the ranges look reasonable?
2. **Revenue by category.** `groupBy("category")` and aggregate: total revenue
   (`F.sum`), average revenue (`F.avg`), and transaction count (`F.count`). Round money
   columns with `F.round(..., 2)`. Order by total revenue descending.
3. **Revenue by region.** Same pattern, `groupBy("region")`. Order descending.
4. **Units sold.** Add `F.sum("quantity")` to one of the rollups to separate *revenue*
   from *volume* — high revenue can come from few expensive items or many cheap ones.

> **SQL bridge:** each rollup is `SELECT category, SUM(revenue), AVG(revenue), COUNT(*)
> FROM t GROUP BY category ORDER BY 2 DESC`. Try writing it both ways (DataFrame API and
> `spark.sql`) to see they're equivalent.

## Expected output

- A `describe` table with one row per statistic across the numeric columns.
- A category table: **Electronics** clearly leads revenue; **Food** is highest in volume
  but lowest in revenue.
- A region table ranked by total revenue, with average order value visibly different
  between regions.

## Checkpoint

- Which category has the **highest total revenue**, and which has the **most units sold**?
  Are they the same? Why does that matter to a merchandiser?
- Why is `describe()` a weak tool for the string columns here?

---

[← Setup](00-setup.md) · [Index](Lab-instructions/index.md) · [Next: 02 · Diagnostic →](Lab-instructions/02-diagnostic-analytics.md)
