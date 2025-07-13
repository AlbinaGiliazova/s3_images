from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from storages.backends.s3boto3 import S3Boto3Storage

from .fixtures import create_test_image, S3TestCase
from s3_avatars.models import Avatar


class AvatarsTestCase(S3TestCase):
    def test_multiple_avatars_for_one_user(self):
        user = User.objects.create_user(username='demo')

        img1 = SimpleUploadedFile(
            'avatar1.png', create_test_image().read(), content_type='image/png'
        )
        img2 = SimpleUploadedFile(
            'avatar2.png',
            create_test_image(color=(0, 255, 0)).read(),
            content_type='image/png',
        )

        avatar1 = Avatar.objects.create(user=user, avatar=img1)
        avatar2 = Avatar.objects.create(user=user, avatar=img2)

        self.assertEqual(
            Avatar.objects.filter(user=user).count(),
            2,
            'Пользователь должен иметь два аватара',
        )
        self.assertNotEqual(
            avatar1.avatar.name,
            avatar2.avatar.name,
            'Аватары должны быть разными файлами',
        )

        # Проверяем, что оба файла лежат в одном и том же s3 бакете
        storage = S3Boto3Storage()

        self.assertTrue(
            storage.exists(avatar1.avatar.name),
            f'Файл {avatar1.avatar.name} не найден в S3 бакете',
        )
        self.assertTrue(
            storage.exists(avatar2.avatar.name),
            f'Файл {avatar2.avatar.name} не найден в S3 бакете',
        )

        # bucket_name совпадает и для первого, и для второго файла
        obj1_bucket = avatar1.avatar.storage.bucket_name
        obj2_bucket = avatar2.avatar.storage.bucket_name
        self.assertEqual(
            obj1_bucket,
            obj2_bucket,
            'Оба файла должны быть в одном S3 бакете, '
            'а не в {obj1_bucket} и {obj2_bucket}',
        )

    def test_user_can_see_other_users_avatars(self):
        user1 = User.objects.create_user(username='first', password='pass1')
        user2 = User.objects.create_user(username='second', password='pass2')

        img = SimpleUploadedFile(
            'avatar.png', create_test_image().read(), content_type='image/png'
        )

        Avatar.objects.create(user=user1, avatar=img)

        client = APIClient()
        client.force_authenticate(user=user2)  # "second" логинится

        response = client.get(f'/api/v1/avatars/?user={user1.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], user1.id)

    def test_anon_user_can_see_other_users_avatars(self):
        user1 = User.objects.create_user(username='first', password='pass1')
        img = SimpleUploadedFile(
            'avatar.png', create_test_image().read(), content_type='image/png'
        )
        Avatar.objects.create(user=user1, avatar=img)

        client = APIClient()  # Клиент НЕ аутентифицирован

        response = client.get(f'/api/v1/avatars/?user={user1.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], user1.id)
