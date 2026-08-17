# 05 · Customer Segmentation — *Champions → At Risk*

Use Case #1. Turn the RFM scores from Part 4 into named, actionable customer segments.

---

## Objective

Map each customer's R/F/M tiers to a business segment, then count how many customers fall
into each — the kind of output a marketing team acts on directly.

## Key concepts

- Raw RFM numbers aren't actionable; **named segments** are. The standard grid keys mostly
  off **Recency** (are they still active?) and a combined **F+M** (how valuable when active?).
- Implement the grid as an ordered `F.when(...).when(...).otherwise(...)` chain — **order
  matters**, because the first matching branch wins.

## Suggested segment rules

Compute an `fm = (F + M) / 2` helper, then apply top-down:

| Segment | Rough rule | Meaning / action |
|---|---|---|
| **Champions** | `R ≥ 4` and `fm ≥ 4` | Best customers — reward, ask for referrals |
| **Loyal** | `fm ≥ 3` | Consistent spenders — upsell |
| **Potential Loyalist** | `R ≥ 3` and `fm ≥ 2` | Recent, promising — nurture |
| **New / Promising** | `R ≥ 3` | Recent but light — onboard, encourage repeat |
| **At Risk** | `R ≤ 2` and `fm ≥ 3` | Were valuable, going quiet — win-back campaign |
| **Hibernating / Lost** | `R ≤ 2` and `fm < 3` | Long gone, low value — low-cost reactivation |
| **Needs Attention** | everything else | Middling — monitor |

> These thresholds are **deliberately tunable** — Exercise 5 asks you to change them and
> watch the segment sizes move. Keep them as named constants so a student can adjust one
> number and re-run.

## Steps

1. Start from the customer-level RFM table (Part 4).
2. Add the `fm` helper column.
3. Build the `segment` column as an ordered `when/otherwise` chain following the table above
   (Champions first, `Needs Attention` as the fallback).
4. `groupBy("segment")` and count to get segment sizes; order by count descending.
5. (Optional) Join segment labels back onto the transaction table so downstream views can
   filter by segment.

## Expected output

- A customer table with a `segment` label per customer.
- A segment-size summary — on this small dataset most segments hold just 1–3 customers, and
  some defined segments may be **empty**. That's expected and worth discussing.

## Checkpoint

- Which customers are **Champions**, and does that agree with their raw `rfm_sum`?
- Why does branch **order** in the `when` chain change the result?
- If you loosen the Champions rule to `fm ≥ 3`, who moves in — and what did you trade away?

---

[← 04 · Feature Engineering](04-predictive-feature-engineering.md) · [Index](index.md) · [Next: 06 · Anomaly Detection →](06-anomaly-detection.md)
