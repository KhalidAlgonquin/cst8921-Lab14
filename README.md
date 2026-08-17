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

<img width="660" height="215" alt="image" src="https://github.com/user-attachments/assets/b3f70c28-53ee-456f-9df4-98d70065eafc" />

Electronics generated the highest revenue, while Food had the highest number of units sold.

### Revenue by Region

<img width="612" height="230" alt="image" src="https://github.com/user-attachments/assets/404fc0d2-49b2-45f3-8cbe-9619b58466b1" />

North generated the highest total revenue.

---

## Part 2 – Diagnostic Analytics

Diagnostic analysis was performed using:

- Region/category pivot tables
- Regional drill-down
- Monthly revenue trends
- Payment-method analysis

### Monthly Revenue

<img width="551" height="202" alt="image" src="https://github.com/user-attachments/assets/4b2e420a-da62-4b9f-9657-a35dc867e614" />

March generated the highest monthly revenue.

Credit-card transactions also had the highest average and total revenue.

---

## Part 3 – Window Functions

Spark window functions were used for:

- Ranking transactions inside each region
<img width="601" height="321" alt="image" src="https://github.com/user-attachments/assets/e5005de9-c4ea-458c-95b7-98741434ebe4" />

- Finding the Top 2 transactions per region
<img width="612" height="228" alt="image" src="https://github.com/user-attachments/assets/6951590a-c395-46f6-8f9f-83d6a2892ddf" />

- Calculating running revenue totals
<img width="617" height="317" alt="image" src="https://github.com/user-attachments/assets/c61a303a-44a1-44ff-af29-4e7c5cbb03c0" />

- Creating revenue quartiles using `ntile()`
<img width="542" height="423" alt="image" src="https://github.com/user-attachments/assets/a0aef374-c8e7-40e3-a711-5836690ed592" />

- Finding the previous customer purchase using `lag()`
<img width="608" height="313" alt="image" src="https://github.com/user-attachments/assets/a141895b-dc04-4f3d-802f-fbbdb9e0f3e1" />


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
<img width="1165" height="313" alt="image" src="https://github.com/user-attachments/assets/85b78608-11b5-4c7b-9c23-8c2e516060a6" />

Customer RFM metrics were then calculated:

- **Recency:** days since latest transaction
- **Frequency:** number of transactions
- **Monetary:** total customer spending
<img width="397" height="207" alt="image" src="https://github.com/user-attachments/assets/01cb3e86-6ac7-4ccd-be3c-74e4d63112ea" />

R, F, and M values were scored from 1 to 4.

Alice received the highest score:

<img width="666" height="167" alt="image" src="https://github.com/user-attachments/assets/0bd76952-3bae-485d-8fa5-b7f49a777047" />

---

## Part 5 – Customer Segmentation

Customers were grouped into business-oriented segments using their RFM scores.

### Segment Summary

<img width="377" height="218" alt="image" src="https://github.com/user-attachments/assets/5a394f11-d40a-4019-8d52-a7c44fae09ef" />

Alice was classified as a **Champion** because of her high recency, frequency, and monetary scores.

---

## Part 6 – Anomaly Detection

Z-score analysis was used to identify unusual transaction revenue.

The threshold used was:

```text
|Z| > 2.0
```

Two global anomalies were detected:

<img width="526" height="177" alt="image" src="https://github.com/user-attachments/assets/f65e4269-5a7b-43bf-913d-104917f6687a" />

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
