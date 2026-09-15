CREATE EXTERNAL TABLE fashion_db.inventory (
    id string,
    gender string,
    masterCategory string,
    subCategory string,
    articleType string,
    baseColour string,
    season string,
    year double,
    usage string,
    productDisplayName string,
    brand_name string
)
STORED AS PARQUET
LOCATION 's3://dtu-fashion-project-2026/processed-parquet/';
