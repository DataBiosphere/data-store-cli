from dbio import DataBiosphereConfig
from dbio.dss import DSSClient
import boto3    

s3 = boto3.resource('s3')
bucket = s3.Bucket('upload-test-unittest') 

dbio_config = DataBiosphereConfig()
dbio_config["DSSClient"].swagger_url = f"https://dss.dev.ucsc-cgp-redwood.org/v1/swagger.json"
dss = DSSClient(config=dbio_config)

print(dss.upload(src_dir="data/", replica="aws", staging_bucket="upload-test-unittest"))
 
bucket.objects.all().delete()

print("Upload successful")
