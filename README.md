# CST8921 - Cloud Industry Trends
# Lab 14: Big Data Analytics with PySpark

### Student: Khalid Amchat  

### Term: S26

---

## Overview

This lab demonstrates big data analytics using **PySpark** on a simulated retail transaction dataset.

The lab covers descriptive and diagnostic analytics, window functions, feature engineering, RFM customer segmentation, anomaly detection, and Parquet storage.

## Technologies Used

- Python 3
- PySpark 4.0.1
- Apache Spark
- Spark DataFrame API
- Parquet

## Setup

A Spark session was created in local mode:

```python
SparkSession.builder \
    .appName("CST8921-Lab14") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()
```

The dataset contains **20 retail transactions**.

Two derived columns were added:

- `revenue = unit_price × quantity`
- `event_time` converted from string to Spark timestamp

---

## Part 1 – Descriptive Analytics

Summary statistics and aggregations were performed using `describe()`, `groupBy()`, and `agg()`.

### Main Results

| Category | Revenue | Units Sold |
|---|---:|---:|
| Electronics | $6,179.47 | 10 |
| Clothing | $800.00 | 9 |
| Food | $739.50 | 28 |

Electronics generated the highest revenue, while Food had the highest number of units sold.

### Revenue by Region

| Region | Revenue |
|---|---:|
| North | $3,427.47 |
| East | $1,953.50 |
| West | $1,267.00 |
| South | $1,071.00 |

North generated the highest total revenue.

---

## Part 2 – Diagnostic Analytics

Diagnostic analysis was performed using:

- Region/category pivot tables
- Regional drill-down
- Monthly revenue trends
- Payment-method analysis

### Monthly Revenue

| Month | Revenue |
|---|---:|
| January | $2,983.98 |
| February | $1,610.00 |
| March | $3,124.99 |

March generated the highest monthly revenue.

Credit-card transactions also had the highest average and total revenue.

---

## Part 3 – Window Functions

Spark window functions were used for:

- Ranking transactions inside each region
- Finding the Top 2 transactions per region
- Calculating running revenue totals
- Creating revenue quartiles using `ntile()`
- Finding the previous customer purchase using `lag()`

The `partitionBy()` function allowed calculations to restart independently for each region or customer.

---

## Part 4 – Feature Engineering and RFM

Additional transaction features were created:

- Hour
- Day
- Day of week
- Month
- Weekend flag
- High-value transaction flag
- High-quantity flag

Customer RFM metrics were then calculated:

- **Recency:** days since latest transaction
- **Frequency:** number of transactions
- **Monetary:** total customer spending

R, F, and M values were scored from 1 to 4.

Alice received the highest score:

```text
R4F4M4
RFM Sum = 12
```

---

## Part 5 – Customer Segmentation

Customers were grouped into business-oriented segments using their RFM scores.

### Segment Summary

| Segment | Customers |
|---|---:|
| Hibernating / Lost | 4 |
| Loyal | 3 |
| Champions | 1 |
| New / Promising | 1 |

Alice was classified as a **Champion** because of her high recency, frequency, and monetary scores.

---

## Part 6 – Anomaly Detection

Z-score analysis was used to identify unusual transaction revenue.

The threshold used was:

```text
|Z| > 2.0
```

Two global anomalies were detected:

| Transaction | Customer | Revenue | Z-score |
|---|---|---:|---:|
| T001 | Alice | $1,799.98 | 2.84 |
| T017 | Grace | $1,560.00 | 2.36 |

When Z-scores were calculated separately for each product category, no transactions exceeded the anomaly threshold.

This shows that an observation can be unusual compared with the complete dataset while still being normal within its own category.

---

## Part 7 – Parquet Data Engineering

The enriched dataset was written to Parquet in three formats:

```text
output/
├── transactions_by_region/
├── transactions_by_month/
└── transactions_non_partitioned/
```

The region-partitioned dataset creates folders such as:

```text
region=North/
region=South/
region=East/
region=West/
```

The month-partitioned dataset creates:

```text
month=1/
month=2/
month=3/
```

The data was read back from Parquet to verify the result.

```text
Original row count : 20
Read-back row count: 20
Row-count verification: PASSED
```

---

## Run the Lab

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the PySpark program:

```bash
python big_data_analytics_lab.py
```

---

## Lessons Learned

From this lab, I learned how to:

- Perform descriptive and diagnostic analytics with PySpark.
- Use Spark window functions for ranking and running calculations.
- Engineer features from timestamp and transaction data.
- Apply RFM analysis to customer behaviour.
- Create customer segments from analytical scores.
- Detect anomalies using Z-scores.
- Store Spark DataFrames efficiently using partitioned Parquet files.
- Read persisted Parquet data back into Spark and validate the results.

## Conclusion

This lab demonstrated how PySpark can be used across the full analytics workflow, from raw transaction data to business insights and optimized data storage.