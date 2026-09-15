<h1 align="center">Multimodal Data Pipeline for Fashion Inventory Intelligence</h1>

<p align="center">
  <em>An end-to-end serverless Data Lakehouse architecture on AWS for multimodal fashion inventory data.</em>
</p>

---

## 📌 Project Overview
In the modern e-commerce landscape, managing diverse datasets ranging from structured metadata to unstructured images is a significant challenge. Traditional systems struggle with "Data Silos," leading to data inconsistency and a lack of real-time insights. 

This project implements an end-to-end, serverless Data Lakehouse architecture on Amazon Web Services (AWS) to ingest, process, and visualize multimodal fashion inventory data. It enriches product data through event-driven ETL and provides an interactive dashboard for inventory auditing.

## 🛠️ Technology Stack
- **Storage Layer:** Amazon S3 (Data Lakehouse)
- **Processing Layer:** AWS Lambda (Python 3.12, Pandas, AWS Data Wrangler)
- **Cataloging Layer:** Amazon Athena (Serverless Schema-on-Read SQL)
- **Visualization Layer:** Amazon QuickSight (Business Intelligence)

## 🗂️ Dataset Description
The system processes 1,000+ fashion products sourced from Kaggle, simulating a real-world multimodal environment across three distinct formats:
1. **Structured Metadata (`styles.csv`):** Core inventory attributes (ID, gender, masterCategory, articleType).
2. **Semi-Structured Attributes (`product_metadata.jsonl`):** Deep, nested attributes including market data (brandName, price) and technical specs.
3. **Unstructured Visual Assets (`.jpg`):** High-resolution product images mapped via unique ID keys.

## ⚙️ Phases of Implementation

### Phase 1: Ingestion & Lake Formation
- Established a centralized Data Lake on Amazon S3 maintaining strict data provenance. 
- Raw assets are partitioned into `raw/images/`, `raw/metadata-csv/`, and `raw/metadata-json/` to preserve their immutable original states.

### Phase 2: Serverless ETL & Enrichment (AWS Lambda)
- Designed a Python-based AWS Lambda function to acquire multi-format data simultaneously.
- Flattened nested JSON structures to dynamically extract keys like `brandName`.
- Executed data type normalization (casting float IDs to standard strings) and performed Relational Left Joins via Pandas.
- Handled null artifacts with categorical imputation (e.g., mapping missing baseColour to "Multi-Color" and season to "All-Season").
- **Optimization:** Converted the processed DataFrame from row-based CSV into columnar **Apache Parquet** format (`processed-parquet/`) to massively reduce downstream query latency and I/O overhead.

### Phase 3: Schema-on-Read Cataloging
- Utilized Amazon Athena to project a structured SQL interface directly over the S3 Parquet files without requiring persistent database servers.
- Created the `fashion_db.inventory` table to act as a dynamic metadata pointer, enabling instant data discovery and high-throughput querying.

### Phase 4: Business Intelligence Visualization
- Developed a cloud-native, multimodal dashboard in Amazon QuickSight integrating text analytics with visual assets.
- Key diagnostic visuals include:
  - **Taxonomy Hierarchy (Treemap):** Visualizing SKU density across sub-categories.
  - **Inventory Flow (Sankey Diagram):** Mapping the relationship between product usage and master categories.
  - **Brand Performance (Bar Chart):** Validating the successful enrichment of JSON metadata (Adidas ranked as top volume).

## 📁 Repository Structure
```text
.
├── src/
│   ├── lambda_function.py      # Primary ETL logic
│   └── athena_schema.sql       # Schema cataloging logic
├── dashboard/                  # Analytical outputs and QuickSight dashboard exports
└── README.md
