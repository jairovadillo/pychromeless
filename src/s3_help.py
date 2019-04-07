import boto3
import botocore

class S3:
    def __init__(self, bucket):
        self.bucket_name = bucket
        self.resource = boto3.resource('s3')
        self.bucket = self.resource.Bucket(bucket)

    def get_key(self, remote_path):
        return self.resource.Object(bucket_name=self.bucket_name, key=remote_path)

    def upload_file(self, local_path, remote_path):
        print(f'[!] Uploading {local_path} to s3://{self.bucket_name}/{remote_path}')
        return self.bucket.upload_file(local_path, remote_path)
        #return self.resource.meta.client.upload_file(local_path,self.bucket_name, remote_path)
