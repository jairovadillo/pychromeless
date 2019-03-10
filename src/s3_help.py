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

    def download_file(self, folder, filename):
        path = folder + filename
        self.resource.Object(self.bucket_name, path).download_file(path)
        return {'screenshot': 'https://{}.s3.amazonaws.com/{}'.format(self.bucket_name, folder) + filename }

    def check_exists(self, folder, filename):
        try:
            return self.download_file(folder, filename)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == "403":
                print("### The object does not exist. Screenshotting... ###")
            else:
                raise
