# Medallion Architecture with AWS Lambda and S3

This repository demonstrates how to implement **Medallion Architecture** using **AWS Lambda** and **Amazon S3**. The architecture organizes data into **Bronze**, **Silver**, and **Gold** layers, progressively transforming raw data into actionable insights.

For a detailed explanation, check out my blog:  
[How to Implement Medallion Architecture Using Lambda and S3](http://13.126.238.20/blogs/blogslist/72d80b10-7ddf-4f3e-8f98-e4f00b5a23e6)

---

## Repository Structure

### Folders

- **`gold_lambda_package/`**  
  Contains the Lambda function code responsible for processing data in the **Silver Layer** and generating aggregated results for the **Gold Layer**, such as counts of customers by region.

- **`silver_lambda_package/`**  
  Contains the Lambda function code responsible for processing raw data from the **Bronze Layer**. This function enriches the data by mapping customer countries to their corresponding regions and outputs the results to the **Silver Layer**.

### Data

- **`dummy_data_1.csv`** and **`dummy_data_2.csv`**  
  Two sample CSV files are included as mock datasets. These files contain columns such as `Customer ID`, `Customer Name`, `Customer Country`, and `Subscription Status`. They can be uploaded to test and validate the architecture.

---

## Workflow

### 1. Bronze Layer

Upload raw customer data (`dummy_data_1.csv` or `dummy_data_2.csv`) into the `bronze/` folder in your S3 bucket.

### 2. Silver Layer

A **Lambda function** from the `silver_lambda_package` will be triggered upon an S3 event. This function:

- Enriches the data by adding a `Region` column based on the `Customer Country`.
- Outputs the transformed data to the `silver/` folder in S3.

### 3. Gold Layer

Another **Lambda function** from the `gold_lambda_package` will process the enriched data in the **Silver Layer**. This function:

- Aggregates data by `Region`, counting unique `Customer IDs`.
- Saves the aggregated data to the `gold/` folder in S3.

This workflow ensures an incremental and scalable transformation of data for analytical purposes.

---

## Setup Instructions

### Prerequisites

- **AWS Account** with S3 and Lambda access.
- **AWS CLI** installed for S3 bucket management.

### Steps

1. **Create an S3 Bucket**  
   Add directories `bronze/`, `silver/`, and `gold/` to your S3 bucket to organize data layers.

2. **Deploy Lambda Functions**

   - Package and deploy the code in the `silver_lambda_package/` for Bronze-to-Silver processing.
   - Package and deploy the code in the `gold_lambda_package/` for Silver-to-Gold aggregation.

3. **Upload Raw Data**  
   Upload the provided `dummy_data_1.csv` or `dummy_data_2.csv` files to the `bronze/` directory in S3.

4. **Monitor Data Transformation**
   - Processed data will appear in the `silver/` directory after the first Lambda function runs.
   - Aggregated data will appear in the `gold/` directory after the second Lambda function completes.

---

## Sample Data Structure

### Raw Data (`Bronze Layer`)

| Customer ID | Customer Name | Customer Country |
| ----------- | ------------- | ---------------- |
| 001         | John Doe      | USA              |

### Enriched Data (`Silver Layer`)

| Customer ID | Customer Name | Customer Country | Region        |
| ----------- | ------------- | ---------------- | ------------- |
| 001         | John Doe      | USA              | North America |

### Aggregated Data (`Gold Layer`)

| Region        | Subscribed Customers | Customer IDs    |
| ------------- | -------------------- | --------------- |
| North America | 150                  | [001, 002, 003] |

---

Simplify data transformations with **AWS Lambda** and **Amazon S3** using the **Medallion Architecture**! 🚀
