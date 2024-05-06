from storages.backends.s3boto3 import S3Boto3Storage

StaticS3BotoStorage = lambda: S3Boto3Storage(location="static")
MediaS3BotoStorage = lambda: S3Boto3Storage(location="media")
