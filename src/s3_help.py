import boto3
import botocore

class S3:
    def __init__(self, bucket):
        self.bucket_name = bucket
        self.resource = boto3.resource('s3')

    def get_key(self, remote_path):
        return self.resource.Object(bucket_name=self.bucket_name, key=remote_path)

    def upload_file(self, key, local_path):
        key.upload_file(local_path)

    def check_exists(self, folder, filename):
        try:
            self.resource.Object(self.bucket_name, folder + filename).load()
            return {'screenshot': 'https://{}.s3.amazonaws.com/{}'.format(self.bucket_name, folder) + filename }
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == "403":
                return False
            else:
                raise
