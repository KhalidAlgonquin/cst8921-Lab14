# 07 · Data Engineering — *Parquet output for downstream use*

Persist the enriched results so other tools (BI, ML, SQL engines) can consume them.

---

## Objective

Write your analytical outputs to partitioned Parquet, then read them back to confirm the
round-trip and schema are intact.

## Key concepts

- **Parquet** is a columnar, compressed, schema-carrying format — the default choice for
  analytics output. Readers can prune columns and skip row groups, so queries touch less data.
- **Partitioning** (`partitionBy`) writes data into subfolders keyed by a column's values
  (e.g. `region=North/`). Downstream filters on that column then skip whole folders
  (*partition pruning*).
- **Write modes:** `overwrite`, `append`, `error` (default), `ignore` — pick deliberately in
  a rerunnable lab so you don't accumulate duplicates.

## Steps

1. **Choose what to persist.** At minimum the enriched transaction table (with `revenue`,
   time features, flags). Optionally also the customer-RFM/segment table and the
   anomaly-flagged table as separate outputs.
2. **Write partitioned Parquet.** `df.write.mode("overwrite").partitionBy("region").parquet(path)`.
   Try partitioning by `region`, then by month, and inspect the folder layout each produces.
3. **Mind partition cardinality.** With only 20 rows, partitioning creates many tiny files —
   the *small-files problem* in miniature. Discuss when to `repartition`/`coalesce` before
   writing in real pipelines.
4. **Read back & verify.** `spark.read.parquet(path)`, then check the row count matches and
   the partition column reappears in the schema (Parquet stores it via the folder path, not
   the file body).
5. **Non-partitioned control.** Write one copy without `partitionBy` and compare the
   directory contents so the effect of partitioning is visible.

> **Teaching note:** Parquet is self-describing — no external schema needed on read. Contrast
> with CSV, which loses types and needs schema inference or a declared schema every time.

## Expected output

- An output directory containing `region=…/` (or `month=…/`) subfolders, each with a
  `.snappy.parquet` file plus a `_SUCCESS` marker.
- A read-back DataFrame whose count and columns match what you wrote.

## Checkpoint

- After writing `partitionBy("region")`, how many subfolders exist and why?
- Where did the `region` values physically go — into the files, or the folder names?
- Why is partitioning by a very high-cardinality column (like `transaction_id`) a bad idea?

---

[← 06 · Anomaly Detection](Lab-instructions/06-anomaly-detection.md) · [Index](Lab-instructions/index.md) · [Next: 08 · Hands-On Exercises →](Lab-instructions/08-hands-on-exercises.md)
