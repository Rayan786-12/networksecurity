# import os

# class S3Sync:
#     def sync_folder_to_s3(self,folder,aws_bucket_url):
#         command=f'aws s3 sync {folder} {aws_bucket_url}'
#         os.system(command)
    
#     def sync_folder_from_s3(self,folder,aws_bucket_url):
#         command=f"aws s3 sync {aws_bucket_url} {folder}"
#         os.system(command)

import os
import boto3
class S3Sync:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str):
        if not aws_bucket_url.startswith("s3://"):
            raise ValueError("AWS Bucket URL must start with s3://")
        bucket = aws_bucket_url.split("/")[2]
        prefix = "/".join(aws_bucket_url.split("/")[3:])

        for root, _, files in os.walk(folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, folder)
                s3_key = f"{prefix}/{relative_path}" if prefix else relative_path
                s3_key = s3_key.replace("\\", "/")  # Windows fix
                print(f"Uploading {local_path} to s3://{bucket}/{s3_key}")
                self.s3.upload_file(local_path, bucket, s3_key)
        