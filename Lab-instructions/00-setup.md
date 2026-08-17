# 00 · Setup

Before any analytics, get the environment running, load the dataset, and add the two
derived columns every later part depends on.

---

## Prerequisites

- Python 3.9+
- PySpark 4.x
- Java 17 — `JAVA_HOME=/opt/homebrew/opt/openjdk@17`
- `JAVA_TOOL_OPTIONS=--add-opens=java.base/javax.security.auth=ALL-UNNAMED`

> If Spark fails to start with a security/`IllegalAccessException` error on a newer JDK, the
> `--add-opens` flag above is the fix. Confirm `java -version` before troubleshooting anything else.

## Run the lab

```bash
python big_data_analytics_lab.py
```

---

## Step 1 — Start a Spark session

Create a local `SparkSession` (`local[*]`), give it an app name, and set the log level to
`ERROR` so the console stays readable. For this tiny dataset, lower
`spark.sql.shuffle.partitions` (e.g. to 4) so shuffles don't spawn 200 empty tasks.

## Step 2 — Load the dataset

Build a DataFrame from the in-memory `transactions` list using the explicit `schema` below.
Using an explicit schema (rather than inferring) is the habit to teach: it makes types
predictable and catches malformed rows early.

## Step 3 — Add the two derived columns

Everything downstream assumes these exist:

1. **`revenue`** = `unit_price * quantity` — round to 2 decimals.
2. **`event_time`** — a real timestamp parsed from the `timestamp` string with
   `to_timestamp`. The raw column is a string; date/time functions in later parts need an
   actual `TimestampType`.

Cache the enriched DataFrame if you'll reuse it across parts (you will).

---

## Dataset (reference)

Simulated retail transactions across four regions, Jan–Mar 2024.

```
transactions = [
    (1,  "T001", "Alice",   "North", "Electronics", 899.99, 2, "2024-01-05 10:30:00", "credit_card"),
    (2,  "T002", "Bob",     "South", "Clothing",     45.00, 3, "2024-01-06 11:00:00", "cash"),
    (3,  "T003", "Charlie", "East",  "Electronics", 199.50, 1, "2024-01-06 14:20:00", "debit_card"),
    (4,  "T004", "Alice",   "North", "Food",          12.50, 5, "2024-01-07 09:15:00", "cash"),
    (5,  "T005", "David",   "West",  "Electronics", 450.00, 1, "2024-01-08 16:45:00", "credit_card"),
    (6,  "T006", "Eve",     "South", "Food",          22.00, 4, "2024-01-08 18:00:00", "credit_card"),
    (7,  "T007", "Frank",   "North", "Clothing",     75.00, 2, "2024-01-09 13:30:00", "debit_card"),
    (8,  "T008", "Grace",   "East",  "Food",          33.00, 3, "2024-01-10 10:00:00", "cash"),
    (9,  "T009", "Heidi",   "West",  "Electronics", 600.00, 1, "2024-02-01 12:00:00", "credit_card"),
    (10, "T010", "Ivan",    "South", "Clothing",    110.00, 2, "2024-02-02 15:30:00", "debit_card"),
    (11, "T011", "Alice",   "North", "Electronics", 250.00, 1, "2024-02-03 09:00:00", "credit_card"),
    (12, "T012", "Bob",     "South", "Food",         18.00, 6, "2024-02-04 17:00:00", "cash"),
    (13, "T013", "Charlie", "East",  "Clothing",     95.00, 1, "2024-02-05 11:45:00", "credit_card"),
    (14, "T014", "David",   "West",  "Food",          8.50, 2, "2024-02-06 08:30:00", "debit_card"),
    (15, "T015", "Eve",     "South", "Electronics", 320.00, 1, "2024-02-07 14:00:00", "credit_card"),
    (16, "T016", "Frank",   "North", "Food",         55.00, 3, "2024-03-01 10:15:00", "cash"),
    (17, "T017", "Grace",   "East",  "Electronics", 780.00, 2, "2024-03-02 16:00:00", "credit_card"),
    (18, "T018", "Heidi",   "West",  "Clothing",    200.00, 1, "2024-03-03 12:30:00", "debit_card"),
    (19, "T019", "Ivan",    "South", "Food",         40.00, 5, "2024-03-04 09:45:00", "cash"),
    (20, "T020", "Alice",   "North", "Electronics", 999.99, 1, "2024-03-05 11:00:00", "credit_card"),
]
```

## Schema (reference)

```
schema = StructType([
    StructField("id",             IntegerType(), True),
    StructField("transaction_id", StringType(),  True),
    StructField("customer",       StringType(),  True),
    StructField("region",         StringType(),  True),
    StructField("category",       StringType(),  True),
    StructField("unit_price",     DoubleType(),  True),
    StructField("quantity",       IntegerType(), True),
    StructField("timestamp",      StringType(),  True),
    StructField("payment_method", StringType(),  True),
])
```

**Good to know before you start:** 9 unique customers, 20 transactions, 4 regions
(North/South/East/West), 3 categories (Electronics/Clothing/Food), 3 payment methods.
The small size is deliberate — you can verify every result by hand.

---

[Index](index.md) · [Next: 01 · Descriptive →](01-descriptive-analytics.md)
