import boto3
import pandas as pd
from io import StringIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get bucket and object key from the event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']  # e.g., silver/input_data.csv

        # Ensure file is in the 'silver' folder
        if not object_key.startswith("silver/"):
            raise ValueError("Uploaded file is not in the 'silver' folder.")

        # Read the CSV file from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
        csv_data = response['Body'].read().decode('utf-8')

        # Load CSV into pandas DataFrame
        df = pd.read_csv(StringIO(csv_data))

        # Group by region and aggregate the customer counts and customer IDs
        region_summary = df.groupby('Region').agg(
            Customer_Count=('Customer Id', 'count'),
            Customer_IDs=('Customer Id', lambda x: ', '.join(map(str, x)))
        ).reset_index()

        # Convert the DataFrame to CSV
        csv_buffer = StringIO()
        region_summary.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        # Save the processed CSV to the 'gold/' folder
        destination_key = f"gold/{object_key.split('/')[-1]}"  # Move from silver/input_data.csv to gold/input_data.csv
        s3_client.put_object(
            Bucket=source_bucket,
            Key=destination_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )

        return {
            'statusCode': 200,
            'body': f"File processed successfully and saved to {source_bucket}/{destination_key}"
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing file: {e}"
        }