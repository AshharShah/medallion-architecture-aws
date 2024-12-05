import boto3
import pandas as pd
from io import StringIO

s3_client = boto3.client('s3')

# Define the country-region mapping dictionary
country_region_mapping = {
    "Chile": "South America",
    "Djibouti": "Africa",
    "Antigua and Barbuda": "Caribbean",
    "Dominican Republic": "Caribbean",
    "Slovakia (Slovak Republic)": "Europe",
    "Bosnia and Herzegovina": "Europe",
    "Pitcairn Islands": "Oceania",
    "Bulgaria": "Europe",
    "Cyprus": "Europe",
    "Timor-Leste": "Asia",
    "Guernsey": "Europe",
    "Vietnam": "Asia",
    "Sri Lanka": "Asia",
    "Singapore": "Asia",
    "Oman": "Asia",
    "Western Sahara": "Africa",
    "Mozambique": "Africa",
    "South Georgia and the South Sandwich Islands": "Antarctica",
    "French Polynesia": "Oceania",
    "Malta": "Europe",
    "Netherlands": "Europe",
    "Paraguay": "South America",
    "Lao People's Democratic Republic": "Asia",
    "Albania": "Europe",
    "Panama": "North America",
    "Belarus": "Europe",
    "Switzerland": "Europe",
    "Saint Vincent and the Grenadines": "Caribbean",
    "Tanzania": "Africa",
    "Zimbabwe": "Africa",
    "Denmark": "Europe",
    "Liechtenstein": "Europe",
    "United States of America": "North America",
    "Bahamas": "Caribbean",
    "Others": "Others"
}

def lambda_handler(event, context):
    try:
        # Get bucket and object key from the event
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']  # e.g., bronze/input_data.csv

        # Ensure file is in the 'bronze' folder
        if not object_key.startswith("bronze/"):
            raise ValueError("Uploaded file is not in the 'bronze' folder.")

        # Read the CSV file from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
        csv_data = response['Body'].read().decode('utf-8')

        # Load CSV into pandas DataFrame
        df = pd.read_csv(StringIO(csv_data))

        # Add a new column for regions based on the country
        def get_region(row):
            country = row['Country']  # Assuming 'Country' is the column name
            return country_region_mapping.get(country, "Others")

        # Apply the get_region function to assign regions
        df['Region'] = df.apply(get_region, axis=1)

        # Convert DataFrame back to CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        # Save the processed CSV to the 'silver/' folder
        destination_key = f"silver/{object_key.split('/')[-1]}"  # Move from bronze/input_data.csv to silver/input_data.csv
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
