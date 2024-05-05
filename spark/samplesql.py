from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, LongType, FloatType, DoubleType, StringType, IntegerType

spark = SparkSession.builder.appName("Sample queries").getOrCreate()

result1 = spark.sql("SELECT * FROM local.nyc.taxis LIMIT 10")


result2 = spark.sql("""
SELECT VendorID, AVG(fare_amount) AS avg_fare, AVG(tip_amount) AS avg_tip
FROM local.nyc.taxis
GROUP BY VendorID
ORDER BY VendorID
""")


result3 = spark.sql("""
SELECT *
FROM local.nyc.taxis
WHERE total_amount > 100
""")


result4 = spark.sql("""
SELECT HOUR(tpep_pickup_datetime) AS pickup_hour, COUNT(*) AS trip_count
FROM local.nyc.taxis
GROUP BY pickup_hour
ORDER BY pickup_hour
""")


result5 = spark.sql("""
SELECT *
FROM local.nyc.taxis
WHERE payment_type = 2 AND passenger_count > 1 AND congestion_surcharge > 0
""")


result6 = spark.sql("""
SELECT RatecodeID, AVG(trip_distance) AS avg_distance, AVG(fare_amount) AS avg_fare, AVG(tip_amount) AS avg_tip, AVG(total_amount) AS avg_total
FROM local.nyc.taxis
WHERE RatecodeID IS NOT NULL
GROUP BY RatecodeID
ORDER BY RatecodeID
""")
result1.collect()
result2.collect()
result3.collect()
result4.collect()

result5.collect()
result6.collect()


windowSpec = Window.partitionBy("VendorID").orderBy("tpep_pickup_datetime").rowsBetween(-10, 0)
df = spark.table("local.nyc.taxis")
result = df.withColumn("running_avg_fare", F.avg("fare_amount").over(windowSpec))

result.collect()

records = spark.sql("""
SELECT * FROM local.nyc.taxis
WHERE passenger_count > 2
""")
records.collect()

spark.sql("""
UPDATE local.nyc.taxis
SET fare_amount = fare_amount + 10
WHERE passenger_count > 2
""")

updated_records = spark.sql("""
SELECT * FROM local.nyc.taxis
WHERE passenger_count > 2
""")
updated_records.collect()

spark.stop()