import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Define constants for better readability and maintainability
# These can also be passed as command-line arguments or configuration files in a real-world scenario.
GCP_PROJECT_ID = "waybackhome-8nw4qqaw543g6sm9h5"
BIGQUERY_DATASET = "way_back_home"
BIGQUERY_TABLE = "sales_fact"
TARGET_AGGREGATE_COLUMN = "qty" # Corrected column name from 'quantity' to 'qty'
GROUP_BY_COLUMN = "location_id"

def main():
    print(f"--- Starting Dataproc BigQuery Extraction and Aggregation Workload for project {GCP_PROJECT_ID} ---")
    
    spark = SparkSession.builder \
        .appName("SalesDataAggregation") \
        .getOrCreate()

    try:
        # Load data from BigQuery
        # Fix 1: Corrected indentation for the 'df' variable assignment.
        # Fix 2: Corrected string quotes for the BigQuery table option.
        # Fix 3: Using explicit 'project' option and 'dataset.table' format for 'table' option for robustness.
        #        The BigQuery table path format is 'project_id.dataset_id.table_id'.
        #        The provided snippet had 'project_id:dataset_id.table_id', which is incorrect for the 'table' option.
        #        It should be 'dataset_id.table_id' when 'project' option is also specified.
        print(f"Attempting to read from BigQuery table: {GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}")
        df = spark.read.format("bigquery") \
            .option("project", GCP_PROJECT_ID) \
            .option("table", f"{BIGQUERY_DATASET}.{BIGQUERY_TABLE}") \
            .load()

        print("Successfully loaded data from BigQuery.")
        print("Schema of the loaded DataFrame:")
        df.printSchema()
        print("First 5 rows of the loaded DataFrame:")
        df.show(5)

        # Perform aggregation
        # Fix 4: Referencing the correct column name 'qty' for aggregation.
        print(f"Aggregating data by '{GROUP_BY_COLUMN}' and summing '{TARGET_AGGREGATE_COLUMN}'...")
        aggregated_df = df.groupBy(GROUP_BY_COLUMN).agg(
            F.sum(TARGET_AGGREGATE_COLUMN).alias(f"total_{TARGET_AGGREGATE_COLUMN}_by_{GROUP_BY_COLUMN}")
        )

        print("Aggregation complete. Displaying results:")
        aggregated_df.show() # Display aggregated results

        # In a production scenario, you would typically write the aggregated_df to a
        # new BigQuery table, GCS, or another persistent storage.
        # Example of writing to a new BigQuery table:
        # output_table_name = f"{BIGQUERY_DATASET}.aggregated_sales_by_location"
        # print(f"Writing aggregated data to BigQuery table: {GCP_PROJECT_ID}.{output_table_name}")
        # aggregated_df.write \
        #     .format("bigquery") \
        #     .option("project", GCP_PROJECT_ID) \
        #     .option("table", output_table_name) \
        #     .mode("overwrite") \
        #     .save()
        # print(f"Aggregated data successfully written.")

        print("Pipeline execution completed successfully!")

    except Exception as e:
        # Added robust error handling
        print(f"An error occurred during the pipeline execution: {e}")
        sys.exit(1) # Exit with a non-zero code to indicate failure
    finally:
        # Ensure Spark Session is stopped gracefully
        spark.stop()
        print("Spark Session stopped.")

if __name__ == "__main__":
    main()