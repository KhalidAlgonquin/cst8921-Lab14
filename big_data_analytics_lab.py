from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)

# ---------------------------------------------------------
# 1. Create Spark session
# ---------------------------------------------------------
spark = (
    SparkSession.builder
    .appName("CST8921-Lab14")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# ---------------------------------------------------------
# 2. Dataset
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 3. Explicit schema
# ---------------------------------------------------------
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

df = spark.createDataFrame(transactions, schema)

# ---------------------------------------------------------
# 4. Derived columns
# ---------------------------------------------------------
df = (
    df
    .withColumn(
        "revenue",
        F.round(F.col("unit_price") * F.col("quantity"), 2)
    )
    .withColumn(
        "event_time",
        F.to_timestamp(F.col("timestamp"))
    )
)

# Cache because later parts reuse this DataFrame
df.cache()

# ---------------------------------------------------------
# 5. Verify the result
# ---------------------------------------------------------
print("\nSchema:")
df.printSchema()

print("\nTransactions:")
df.show(20, truncate=False)

print("Number of rows:", df.count())

# =========================================================
# PART 1 - DESCRIPTIVE ANALYTICS
# =========================================================

print("\n==============================")
print("PART 1 - DESCRIPTIVE ANALYTICS")
print("==============================")

# ---------------------------------------------------------
# 1. Summary statistics
# ---------------------------------------------------------
print("\nSummary Statistics:")

df.select(
    "unit_price",
    "quantity",
    "revenue"
).describe().show()


# ---------------------------------------------------------
# 2. Revenue by category
# ---------------------------------------------------------
print("\nRevenue by Category:")

category_summary = (
    df.groupBy("category")
    .agg(
        F.round(F.sum("revenue"), 2).alias("total_revenue"),
        F.round(F.avg("revenue"), 2).alias("avg_revenue"),
        F.count("*").alias("transaction_count"),
        F.sum("quantity").alias("units_sold")
    )
    .orderBy(F.desc("total_revenue"))
)

category_summary.show()


# ---------------------------------------------------------
# 3. Revenue by region
# ---------------------------------------------------------
print("\nRevenue by Region:")

region_summary = (
    df.groupBy("region")
    .agg(
        F.round(F.sum("revenue"), 2).alias("total_revenue"),
        F.round(F.avg("revenue"), 2).alias("avg_revenue"),
        F.count("*").alias("transaction_count"),
        F.sum("quantity").alias("units_sold")
    )
    .orderBy(F.desc("total_revenue"))
)

region_summary.show()

# =========================================================
# PART 2 - DIAGNOSTIC ANALYTICS
# =========================================================

print("\n==============================")
print("PART 2 - DIAGNOSTIC ANALYTICS")
print("==============================")

# ---------------------------------------------------------
# 1. Region x Category Pivot
# ---------------------------------------------------------
print("\nRevenue by Region and Category:")

region_category_pivot = (
    df.groupBy("region")
    .pivot("category")
    .agg(F.round(F.sum("revenue"), 2))
    .orderBy("region")
)

region_category_pivot.show()


# ---------------------------------------------------------
# 2. Drill-down into the top region
# ---------------------------------------------------------
print("\nDrill-down for Top Region - North:")

north_transactions = (
    df.filter(F.col("region") == "North")
    .select(
        "transaction_id",
        "customer",
        "category",
        "quantity",
        "revenue"
    )
    .orderBy(F.desc("revenue"))
)

north_transactions.show(truncate=False)


# ---------------------------------------------------------
# 3. Monthly Revenue Trend
# ---------------------------------------------------------
print("\nMonthly Revenue Trend:")

monthly_trend = (
    df.withColumn(
        "month",
        F.date_format(F.col("event_time"), "yyyy-MM")
    )
    .groupBy("month")
    .agg(
        F.round(F.sum("revenue"), 2).alias("total_revenue"),
        F.count("*").alias("transaction_count")
    )
    .orderBy("month")
)

monthly_trend.show()


# ---------------------------------------------------------
# 4. Optional - Monthly Revenue by Category
# ---------------------------------------------------------
print("\nMonthly Revenue by Category:")

monthly_category = (
    df.withColumn(
        "month",
        F.date_format(F.col("event_time"), "yyyy-MM")
    )
    .groupBy("month", "category")
    .agg(
        F.round(F.sum("revenue"), 2).alias("total_revenue")
    )
    .orderBy("month", F.desc("total_revenue"))
)

monthly_category.show()


# ---------------------------------------------------------
# 5. Payment Method Analysis
# ---------------------------------------------------------
print("\nAverage Revenue by Payment Method:")

payment_summary = (
    df.groupBy("payment_method")
    .agg(
        F.round(F.avg("revenue"), 2).alias("avg_revenue"),
        F.round(F.sum("revenue"), 2).alias("total_revenue"),
        F.count("*").alias("transaction_count")
    )
    .orderBy(F.desc("avg_revenue"))
)

payment_summary.show()

# =========================================================
# PART 3 - WINDOW FUNCTIONS
# =========================================================

print("\n==============================")
print("PART 3 - WINDOW FUNCTIONS")
print("==============================")

# ---------------------------------------------------------
# 1. Rank transactions within each region
# ---------------------------------------------------------
print("\nTransaction Ranking by Region:")

region_rank_window = (
    Window
    .partitionBy("region")
    .orderBy(F.desc("revenue"))
)

ranked_df = (
    df.withColumn(
        "revenue_rank",
        F.rank().over(region_rank_window)
    )
)

ranked_df.select(
    "region",
    "transaction_id",
    "customer",
    "category",
    "revenue",
    "revenue_rank"
).orderBy("region", "revenue_rank").show(20, truncate=False)


# ---------------------------------------------------------
# 2. Top 2 transactions per region
# ---------------------------------------------------------
print("\nTop 2 Transactions per Region:")

top_2_region = (
    ranked_df
    .filter(F.col("revenue_rank") <= 2)
    .select(
        "region",
        "transaction_id",
        "customer",
        "category",
        "revenue",
        "revenue_rank"
    )
    .orderBy("region", "revenue_rank")
)

top_2_region.show(truncate=False)


# ---------------------------------------------------------
# 3. Running revenue total by region
# ---------------------------------------------------------
print("\nRunning Revenue Total by Region:")

running_window = (
    Window
    .partitionBy("region")
    .orderBy("event_time")
    .rowsBetween(
        Window.unboundedPreceding,
        Window.currentRow
    )
)

running_total_df = (
    df.withColumn(
        "running_revenue",
        F.round(
            F.sum("revenue").over(running_window),
            2
        )
    )
)

running_total_df.select(
    "region",
    "transaction_id",
    "event_time",
    "revenue",
    "running_revenue"
).orderBy("region", "event_time").show(20, truncate=False)


# ---------------------------------------------------------
# 4. Revenue quartiles
# ---------------------------------------------------------
print("\nRevenue Quartiles:")

quartile_window = Window.orderBy(F.desc("revenue"))

quartile_df = (
    df.withColumn(
        "revenue_quartile",
        F.ntile(4).over(quartile_window)
    )
)

quartile_df.select(
    "transaction_id",
    "customer",
    "region",
    "revenue",
    "revenue_quartile"
).orderBy(F.desc("revenue")).show(20, truncate=False)


# ---------------------------------------------------------
# 5. Previous purchase revenue for each customer
# ---------------------------------------------------------
print("\nPrevious Purchase Revenue by Customer:")

customer_window = (
    Window
    .partitionBy("customer")
    .orderBy("event_time")
)

previous_purchase_df = (
    df.withColumn(
        "prev_revenue",
        F.lag("revenue").over(customer_window)
    )
)

previous_purchase_df.select(
    "customer",
    "transaction_id",
    "event_time",
    "revenue",
    "prev_revenue"
).orderBy("customer", "event_time").show(20, truncate=False)

# =========================================================
# PART 4 - FEATURE ENGINEERING AND RFM
# =========================================================

print("\n==========================================")
print("PART 4 - FEATURE ENGINEERING AND RFM")
print("==========================================")


# ---------------------------------------------------------
# 1. Calculate average revenue
#    Used as threshold for high-value transactions
# ---------------------------------------------------------
average_revenue = (
    df.agg(F.avg("revenue").alias("avg_revenue"))
    .first()["avg_revenue"]
)

print(f"\nAverage Revenue Threshold: {average_revenue:.2f}")


# ---------------------------------------------------------
# 2. Transaction-level feature engineering
# ---------------------------------------------------------
featured_df = (
    df
    .withColumn("hour", F.hour("event_time"))
    .withColumn("day", F.dayofmonth("event_time"))
    .withColumn("dayofweek", F.dayofweek("event_time"))
    .withColumn("month", F.month("event_time"))

    # Saturday = 7, Sunday = 1 in Spark
    .withColumn(
        "is_weekend",
        F.when(
            F.col("dayofweek").isin(1, 7),
            1
        ).otherwise(0)
    )

    # Revenue higher than dataset average
    .withColumn(
        "is_high_value",
        F.when(
            F.col("revenue") > average_revenue,
            1
        ).otherwise(0)
    )

    # Quantity greater than 3
    .withColumn(
        "high_quantity",
        F.when(
            F.col("quantity") > 3,
            1
        ).otherwise(0)
    )
)

print("\nTransaction-Level Features:")

featured_df.select(
    "transaction_id",
    "customer",
    "event_time",
    "revenue",
    "quantity",
    "hour",
    "day",
    "dayofweek",
    "month",
    "is_weekend",
    "is_high_value",
    "high_quantity"
).show(20, truncate=False)

# ---------------------------------------------------------
# 3. Reference date for Recency
# ---------------------------------------------------------
reference_date = (
    df.agg(
        F.max("event_time").alias("reference_date")
    )
    .first()["reference_date"]
)

print("\nRFM Reference Date:", reference_date)

# ---------------------------------------------------------
# 4. Customer-level RFM metrics
# ---------------------------------------------------------
rfm_df = (
    df.groupBy("customer")
    .agg(
        F.datediff(
            F.lit(reference_date),
            F.max("event_time")
        ).alias("recency_days"),

        F.count("*").alias("frequency"),

        F.round(
            F.sum("revenue"),
            2
        ).alias("monetary")
    )
)

print("\nRaw RFM Metrics:")

rfm_df.orderBy("recency_days").show(truncate=False)

# ---------------------------------------------------------
# 5. RFM scoring windows
# ---------------------------------------------------------

# Recency:
# smaller number of days = better
recency_window = Window.orderBy(
    F.col("recency_days").asc(),
    F.col("customer").asc()
)

# Frequency:
# larger number of purchases = better
frequency_window = Window.orderBy(
    F.col("frequency").asc(),
    F.col("customer").asc()
)

# Monetary:
# larger spending = better
monetary_window = Window.orderBy(
    F.col("monetary").asc(),
    F.col("customer").asc()
)

# ---------------------------------------------------------
# 6. Add R, F, and M scores
# ---------------------------------------------------------
rfm_scored_df = (
    rfm_df

    # ntile gives recent customers a low tile,
    # so invert it: 5 - tile
    .withColumn(
        "R",
        5 - F.ntile(4).over(recency_window)
    )

    .withColumn(
        "F",
        F.ntile(4).over(frequency_window)
    )

    .withColumn(
        "M",
        F.ntile(4).over(monetary_window)
    )

    .withColumn(
        "rfm_sum",
        F.col("R") + F.col("F") + F.col("M")
    )

    .withColumn(
        "rfm_cell",
        F.concat(
            F.lit("R"),
            F.col("R"),
            F.lit("F"),
            F.col("F"),
            F.lit("M"),
            F.col("M")
        )
    )
)


print("\nRFM Scores:")

rfm_scored_df.select(
    "customer",
    "recency_days",
    "frequency",
    "monetary",
    "R",
    "F",
    "M",
    "rfm_sum",
    "rfm_cell"
).orderBy(F.desc("rfm_sum")).show(truncate=False)

# =========================================================
# PART 5 - CUSTOMER SEGMENTATION
# =========================================================

print("\n================================")
print("PART 5 - CUSTOMER SEGMENTATION")
print("================================")


# ---------------------------------------------------------
# 1. Threshold constants
# ---------------------------------------------------------
CHAMPION_R = 4
CHAMPION_FM = 4

LOYAL_FM = 3

POTENTIAL_R = 3
POTENTIAL_FM = 2

NEW_R = 3

AT_RISK_R = 2
AT_RISK_FM = 3


# ---------------------------------------------------------
# 2. Calculate combined Frequency + Monetary score
# ---------------------------------------------------------
segmented_df = (
    rfm_scored_df
    .withColumn(
        "fm",
        (F.col("F") + F.col("M")) / 2
    )
)


# ---------------------------------------------------------
# 3. Assign customer segments
# ---------------------------------------------------------
segmented_df = (
    segmented_df
    .withColumn(
        "segment",

        F.when(
            (F.col("R") >= CHAMPION_R) &
            (F.col("fm") >= CHAMPION_FM),
            "Champions"
        )

        .when(
            F.col("fm") >= LOYAL_FM,
            "Loyal"
        )

        .when(
            (F.col("R") >= POTENTIAL_R) &
            (F.col("fm") >= POTENTIAL_FM),
            "Potential Loyalist"
        )

        .when(
            F.col("R") >= NEW_R,
            "New / Promising"
        )

        .when(
            (F.col("R") <= AT_RISK_R) &
            (F.col("fm") >= AT_RISK_FM),
            "At Risk"
        )

        .when(
            (F.col("R") <= 2) &
            (F.col("fm") < 3),
            "Hibernating / Lost"
        )

        .otherwise(
            "Needs Attention"
        )
    )
)


# ---------------------------------------------------------
# 4. Display customer segments
# ---------------------------------------------------------
print("\nCustomer Segments:")

segmented_df.select(
    "customer",
    "R",
    "F",
    "M",
    "fm",
    "rfm_sum",
    "segment"
).orderBy(
    F.desc("rfm_sum")
).show(truncate=False)


# ---------------------------------------------------------
# 5. Count customers by segment
# ---------------------------------------------------------
print("\nSegment Summary:")

segment_summary = (
    segmented_df
    .groupBy("segment")
    .agg(
        F.count("*").alias("customer_count")
    )
    .orderBy(
        F.desc("customer_count")
    )
)

segment_summary.show(truncate=False)

# =========================================================
# PART 6 - ANOMALY DETECTION
# =========================================================

print("\n==============================")
print("PART 6 - ANOMALY DETECTION")
print("==============================")

THRESHOLD = 2.0


# ---------------------------------------------------------
# 1. Global revenue statistics
# ---------------------------------------------------------
global_stats = (
    df.agg(
        F.mean("revenue").alias("mean_revenue"),
        F.stddev("revenue").alias("stddev_revenue")
    )
)

print("\nGlobal Revenue Statistics:")
global_stats.show()


# ---------------------------------------------------------
# 2. Calculate global Z-score
# ---------------------------------------------------------
global_anomaly_df = (
    df
    .crossJoin(F.broadcast(global_stats))
    .withColumn(
        "z",
        (F.col("revenue") - F.col("mean_revenue"))
        / F.col("stddev_revenue")
    )
    .withColumn(
        "is_anomaly",
        F.abs(F.col("z")) > THRESHOLD
    )
)


print("\nTransactions with Global Z-Scores:")

global_anomaly_df.select(
    "transaction_id",
    "customer",
    "category",
    "revenue",
    F.round("z", 2).alias("z"),
    "is_anomaly"
).orderBy(F.desc("revenue")).show(20, truncate=False)


# ---------------------------------------------------------
# 3. Show only global anomalies
# ---------------------------------------------------------
print("\nGlobal Anomalies:")

global_anomaly_df.filter(
    F.col("is_anomaly") == True
).select(
    "transaction_id",
    "customer",
    "category",
    "revenue",
    F.round("z", 2).alias("z")
).orderBy(F.desc(F.abs("z"))).show(truncate=False)


# ---------------------------------------------------------
# 4. Per-category Z-score
# ---------------------------------------------------------
category_window = Window.partitionBy("category")

category_anomaly_df = (
    df
    .withColumn(
        "category_mean",
        F.mean("revenue").over(category_window)
    )
    .withColumn(
        "category_stddev",
        F.stddev("revenue").over(category_window)
    )
    .withColumn(
        "category_z",
        (F.col("revenue") - F.col("category_mean"))
        / F.col("category_stddev")
    )
    .withColumn(
        "is_category_anomaly",
        F.abs(F.col("category_z")) > THRESHOLD
    )
)


print("\nPer-Category Z-Scores:")

category_anomaly_df.select(
    "transaction_id",
    "customer",
    "category",
    "revenue",
    F.round("category_z", 2).alias("category_z"),
    "is_category_anomaly"
).orderBy(
    "category",
    F.desc("revenue")
).show(20, truncate=False)


# ---------------------------------------------------------
# 5. Show only per-category anomalies
# ---------------------------------------------------------
print("\nPer-Category Anomalies:")

category_anomaly_df.filter(
    F.col("is_category_anomaly") == True
).select(
    "transaction_id",
    "customer",
    "category",
    "revenue",
    F.round("category_z", 2).alias("category_z")
).show(truncate=False)

# =========================================================
# PART 7 - DATA ENGINEERING: PARQUET OUTPUT
# =========================================================

print("\n==========================================")
print("PART 7 - DATA ENGINEERING: PARQUET OUTPUT")
print("==========================================")


# ---------------------------------------------------------
# 1. Output paths
# ---------------------------------------------------------
region_output_path = "output/transactions_by_region"
month_output_path = "output/transactions_by_month"
control_output_path = "output/transactions_non_partitioned"


# ---------------------------------------------------------
# 2. Write Parquet partitioned by region
# ---------------------------------------------------------
print("\nWriting Parquet partitioned by region...")

featured_df.write \
    .mode("overwrite") \
    .partitionBy("region") \
    .parquet(region_output_path)

print("Region-partitioned Parquet written successfully.")


# ---------------------------------------------------------
# 3. Write Parquet partitioned by month
# ---------------------------------------------------------
print("\nWriting Parquet partitioned by month...")

featured_df.write \
    .mode("overwrite") \
    .partitionBy("month") \
    .parquet(month_output_path)

print("Month-partitioned Parquet written successfully.")


# ---------------------------------------------------------
# 4. Write non-partitioned Parquet for comparison
# ---------------------------------------------------------
print("\nWriting non-partitioned Parquet...")

featured_df.write \
    .mode("overwrite") \
    .parquet(control_output_path)

print("Non-partitioned Parquet written successfully.")


# ---------------------------------------------------------
# 5. Read the region-partitioned data back
# ---------------------------------------------------------
print("\nReading region-partitioned Parquet back...")

parquet_df = spark.read.parquet(region_output_path)


# ---------------------------------------------------------
# 6. Verify row count
# ---------------------------------------------------------
original_count = featured_df.count()
readback_count = parquet_df.count()

print(f"Original row count : {original_count}")
print(f"Read-back row count: {readback_count}")

if original_count == readback_count:
    print("Row-count verification: PASSED")
else:
    print("Row-count verification: FAILED")


# ---------------------------------------------------------
# 7. Verify schema
# ---------------------------------------------------------
print("\nRead-back Schema:")

parquet_df.printSchema()


# ---------------------------------------------------------
# 8. Display read-back data
# ---------------------------------------------------------
print("\nRead-back Data:")

parquet_df.select(
    "transaction_id",
    "customer",
    "region",
    "category",
    "revenue",
    "month",
    "is_weekend",
    "is_high_value",
    "high_quantity"
).orderBy("transaction_id").show(20, truncate=False)


# ---------------------------------------------------------
# Stop Spark session
# ---------------------------------------------------------
spark.stop()