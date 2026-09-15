import pandas as pd
import awswrangler as wr

def lambda_handler(event, context):
    bucket = "dtu-fashion-project-2026"
    csv_path = f"s3://{bucket}/raw/metadata-csv/styles.csv"
    jsonl_path = f"s3://{bucket}/raw/metadata-json/product_metadata.jsonl"
    output_path = f"s3://{bucket}/processed-parquet/unified_inventory.parquet"

    try:
        # Load Data from S3 Data Lake
        df_csv = wr.s3.read_csv(path=csv_path)
        df_json = wr.s3.read_json(path=jsonl_path, lines=True)

        # 1. Extract 'brandName' from nested JSON metadata
        df_json['brand_name'] = df_json['data'].apply(lambda x: x.get('brandName', 'Unknown') if isinstance(x, dict) else 'Unknown')
        df_json['id_raw'] = df_json['data'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)

        # 2. Normalization: Ensuring IDs are clean strings for the join key
        df_csv['id'] = pd.to_numeric(df_csv['id'], errors='coerce').fillna(0).astype(int).astype(str)
        df_json['id_join'] = pd.to_numeric(df_json['id_raw'], errors='coerce').fillna(0).astype(int).astype(str)

        # 3. Perform the Left Join
        unified_df = pd.merge(df_csv, df_json[['id_join', 'brand_name']], left_on='id', right_on='id_join', how='left')

        # 4. Cleaning & Imputation (Handling Missing Values)
        unified_df['brand_name'] = unified_df['brand_name'].fillna("Generic")
        unified_df['baseColour'] = unified_df['baseColour'].fillna("Multi-Color")
        unified_df['season'] = unified_df['season'].fillna("All-Season")

        # Drop the temporary join column
        unified_df.drop(columns=['id_join'], inplace=True)

        # 5. Save back to S3 as highly optimized Columnar Parquet format
        wr.s3.to_parquet(df=unified_df, path=output_path, index=False)

        print(f"Success! Joined {len(unified_df)} rows. Cleaned baseColour and season.")
        return {'statusCode': 200, 'body': "ETL Processed with Brand and Cleaning applied."}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}
