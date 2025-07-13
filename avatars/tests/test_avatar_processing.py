from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from storages.backends.s3boto3 import S3Boto3Storage

from s3_avatars.models import CustomUser, Avatar
from .fixtures import create_test_image, S3TestCase


class AvatarProcessingTestCase(S3TestCase):
    def test_avatar_processing(self):
        # 1. Генерируем и загружаем файл
        orig_img = create_test_image()
        orig_size = orig_img.getbuffer().nbytes
        img_file = SimpleUploadedFile(
            'avatar_orig.jpg', orig_img.read(), content_type='image/jpeg'
        )

        user = CustomUser.objects.create_user(username='demo')
        avatar_obj = Avatar.objects.create(user=user, avatar=img_file)
        avatar_obj.refresh_from_db()

        # 2. Проверяем уменьшение размера
        processed_size = avatar_obj.avatar.size
        self.assertLess(processed_size, orig_size, 'Файл не был сжат')

        # 3. Проверяем квадратность
        avatar_obj.avatar.open()
        avatar_img = Image.open(avatar_obj.avatar)
        self.assertEqual(avatar_img.width, avatar_img.height, 'Файл не стал квадратным')

        # 4. Проверяем, что файл физически лежит в бакете
        storage = S3Boto3Storage()
        self.assertTrue(
            storage.exists(avatar_obj.avatar.name), 'Файл не найден в S3 бакете'
        )
