import io
import boto3
from PIL import Image
from django.conf import settings
import botocore
from django.test import TestCase, override_settings
import contextlib


def create_test_image(format='PNG', size=(300, 200), color=(255, 0, 0)):
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
    try:
        s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    except botocore.exceptions.ClientError as e:
        errorcode = e.response['Error']['Code']
        if errorcode != 'BucketAlreadyOwnedByYou':
            raise
    return s3


class S3TestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.override = override_settings(
            AWS_STORAGE_BUCKET_NAME='avatars',
            AWS_S3_ENDPOINT_URL='http://minio:9000',
            AWS_ACCESS_KEY_ID='minioadmin',
            AWS_SECRET_ACCESS_KEY='miniopassword',
            AWS_S3_REGION_NAME='us-east-1',
        )
        cls.override.enable()
        setup_s3_bucket()

    @classmethod
    def cleanup_s3_bucket(cls):
        s3 = boto3.resource(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        # Удаляем все объекты в бакете
        bucket.objects.all().delete()
        # Мягко игнорируем ошибку если бакета нет:
        with contextlib.suppress(Exception):
            bucket.delete()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_s3_bucket()
        cls.override.disable()
        super().tearDownClass()
