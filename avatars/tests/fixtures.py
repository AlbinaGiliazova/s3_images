import io
import boto3
from PIL import Image
from django.conf import settings


def create_test_image(format='JPEG', size=(300, 200), color=(255, 0, 0)):
    file = io.BytesIO()
    Image.new('RGB', size, color).save(file, format)
    file.seek(0)
    return file


def setup_s3_bucket():
    s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    return s3


def cleanup_s3_bucket(s3):
    resp = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    for obj in resp.get('Contents', []):
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=obj['Key'])
