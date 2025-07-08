from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.auth.models import User

from s3_avatars.models import UserProfile
from fixtures import create_test_image, setup_s3_bucket, cleanup_s3_bucket


@override_settings(
    AWS_ACCESS_KEY_ID='minioadmin',
    AWS_SECRET_ACCESS_KEY='minioadmin',
    AWS_STORAGE_BUCKET_NAME='avatars-test',
    AWS_S3_REGION_NAME='us-east-1',
    AWS_S3_ENDPOINT_URL='http://localhost:9000',  # для локального теста
    DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage',
)
class AvatarProcessingTestCase(TestCase):
    def setUp(self):
        self.s3 = setup_s3_bucket()

    def test_avatar_processing(self):
        # 1. Генерируем и загружаем файл
        orig_img = create_test_image()
        orig_size = orig_img.getbuffer().nbytes
        img_file = SimpleUploadedFile(
            'avatar_orig.jpg', orig_img.read(), content_type='image/jpeg'
        )

        user = User.objects.create_user(username='demo')
        profile = UserProfile.objects.create(user=user, avatar=img_file)

        # 2. Проверяем уменьшение размера
        processed_size = profile.avatar.size
        self.assertLess(processed_size, orig_size, 'Файл не был сжат')

        # 3. Проверяем квадратность
        profile.avatar.open()
        avatar_img = Image.open(profile.avatar)
        self.assertEqual(avatar_img.width, avatar_img.height, 'Файл не стал квадратным')

        # 4. Проверяем, что файл физически лежит в бакете

        storage = S3Boto3Storage()
        self.assertTrue(
            storage.exists(profile.avatar.name), 'Файл не найден в S3 бакете'
        )

    def tearDown(self):
        cleanup_s3_bucket(self.s3)
