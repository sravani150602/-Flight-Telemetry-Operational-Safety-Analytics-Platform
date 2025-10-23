from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when
from pyspark.sql.types import *
import json

# Initialize Spark
print("Initializing Spark...")
spark = SparkSession.builder \
    .appName("FlightDataCleaning") \
    .master("local[*]") \
    .getOrCreate()

# Load your raw JSON file
print("Loading raw data from Bronze layer...")
raw_file = "../data/raw_flights_20251021_183758.json"

# Read JSON
with open(raw_file, 'r') as f:
    data = json.load(f)

# Define schema for flight data
schema = StructType([
    StructField("icao24", StringType(), True),
    StructField("callsign", StringType(), True),
    StructField("origin_country", StringType(), True),
    StructField("time_position", LongType(), True),
    StructField("last_contact", LongType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("baro_altitude", DoubleType(), True),
    StructField("on_ground", BooleanType(), True),
    StructField("velocity", DoubleType(), True),
    StructField("true_track", DoubleType(), True),
    StructField("vertical_rate", DoubleType(), True),
    StructField("sensors", StringType(), True),
    StructField("geo_altitude", DoubleType(), True),
    StructField("squawk", StringType(), True),
    StructField("spi", BooleanType(), True),
    StructField("position_source", IntegerType(), True)
])

# Create DataFrame
print("Creating Spark DataFrame...")
df = spark.createDataFrame(data['states'], schema=schema)

print(f"Total records loaded: {df.count()}")

# DATA CLEANING STEPS
print("\n--- Starting Data Cleaning ---")

# 1. Remove null coordinates (can't track flights without position)
df_clean = df.filter(
    (col("latitude").isNotNull()) & 
    (col("longitude").isNotNull())
)
print(f"After removing null coordinates: {df_clean.count()} records")

# 2. Clean callsigns (trim whitespace)
df_clean = df_clean.withColumn("callsign", trim(col("callsign")))

# 3. Remove flights with invalid altitude (negative or too high)
df_clean = df_clean.filter(
    (col("baro_altitude") >= 0) & 
    (col("baro_altitude") <= 50000)
)
print(f"After altitude validation: {df_clean.count()} records")

# 4. Remove duplicate records (same icao24 at same time)
df_clean = df_clean.dropDuplicates(["icao24", "last_contact"])
print(f"After deduplication: {df_clean.count()} records")

# 5. Add data quality flag
df_clean = df_clean.withColumn(
    "data_quality",
    when((col("velocity").isNull()) | (col("true_track").isNull()), "incomplete")
    .otherwise("complete")
)

# Show sample of cleaned data
print("\n--- Sample Cleaned Data ---")
df_clean.select("callsign", "origin_country", "latitude", "longitude", 
                "baro_altitude", "velocity", "data_quality").show(5)

# Save to Silver layer as Parquet
output_path = "../silver/flights_cleaned_20251021.parquet"
print(f"\nSaving cleaned data to: {output_path}")
df_clean.write.mode("overwrite").parquet(output_path)

print("\n✅ Silver layer created successfully!")
print(f"Final record count: {df_clean.count()}")

# Stop Spark
spark.stop()