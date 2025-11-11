import requests
import pandas as pd
import sqlalchemy 
from dotenv import load_dotenv
import os
import json
import boto3
from datetime import datetime
from io import BytesIO, StringIO
from mypy_boto3_s3 import S3Client

load_dotenv()

API_KEY = os.getenv("EIA_API_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")

url = (
"https://api.eia.gov/v2/electricity/retail-sales/data/"
"?frequency=monthly&data[0]=customers&data[1]=price&data[2]=revenue&data[3]=sales"
"&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
)


response = requests.get(f"{url}&api_key={API_KEY}", timeout=10)
response.raise_for_status()
data = response.json()

records = data.get("response", {}).get("data", [])
eia_df = pd.json_normalize(records)

s3_client: S3Client = boto3.client("s3", aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name = REGION)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
raw_key = f"raw_eia/raw_eia_{timestamp}.json"
csv_key = f"clean_eia/clean_eia_{timestamp}.csv"

eia_df.drop(
    columns=[col for col in eia_df.columns if col.endswith("-units")],
    inplace=True
)

raw_buffer = BytesIO()
raw_buffer.write(json.dumps(data, indent=4).encode("utf-8"))
raw_buffer.seek(0)
s3_client.upload_fileobj(raw_buffer, S3_BUCKET, raw_key)
					
csv_buffer = BytesIO()
eia_df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)
s3_client.upload_fileobj(csv_buffer, S3_BUCKET, csv_key)


