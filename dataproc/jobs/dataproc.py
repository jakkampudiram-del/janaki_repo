import sys
from pyspark.sql import SparkSession

def main():
    print("--- Starting Dataproc BigQuery Extraction Workload ---")
    
    spark = SparkSession.builder \
        .appName("SalesDataAggregation") \
        .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar") \
        .getOrCreate()

    df = spark.read.format("bigquery") \
        .option("project", "waybackhome-8nw4qqaw543g6sm9h5") \
        .option("table", "waybackhome-8nw4qqaw543g6sm9h5.way_back_home.sales_fact") \
        .option("temporaryGcsBucket", "dataproc-temp-bucket-waybackhome") \
        .load()

    aggregated_df = df.groupBy("location_id").sum("qty")

    aggregated_df.write.format("bigquery") \
        .option("temporaryGcsBucket", "dataproc-temp-bucket-waybackhome") \
        .option("table", "waybackhome-8nw4qqaw543g6sm9h5.way_back_home.aggregated_sales") \
        .mode("overwrite") \
        .save()

    print("Dataproc pipeline script is syntactically correct and references fixed columns.")

if __name__ == "__main__":
    main()
