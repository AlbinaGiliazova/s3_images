Django: обработка и загрузка аватара с сохранением в S3

Кратко  
Проект автоматически сжимает и обрезает аватары (до квадратной формы), затем сохраняет их в S3-совместимое хранилище.  
Используется Django, Pillow, boto3 и MinIO (локальный S3).
Должен быть установлен Docker.

Как запустить проект

1. Клонируйте репозиторий  
git clone <ссылка на репозиторий>  
cd avatars

2. Запустите инфраструктуру  
docker-compose up --build

3. Проведите миграции  
docker-compose exec django python manage.py migrate

4. Запустите тесты  
docker-compose exec django python manage.py test tests

Ожидается:  
- Ваш аватар уменьшен по размеру  
- Сторона изображения стала квадратной  
- Файл лежит в S3 (MinIO)

Тестовые креденшелы/конфиг S3
Стандартные параметры подключены через docker-compose в виде переменных окружения (см. docker-compose.yml и ваш settings.py): переименуйте .env.example в .env и подставьте свои параметры.

S3 (MinIO) доступен по адресу:  
http://localhost:9001  
Логин: minioadmin  
Пароль: miniopassword

Пояснения по архитектуре

- Обработка изображений — через Pillow (resize, crop, сжатие JPEG, PNG)
- Сохранение — через кастомный Storage-класс, основанный на boto3/django-storages
- Хранилище S3 (MinIO) полностью локальное — настройка в docker-compose

Важные команды

- docker-compose up — старт всего проекта  
- docker-compose exec django python manage.py migrate — миграции  
- docker-compose exec django python manage.py test tests — тесты  
- docker-compose down — остановить проект

Контакты/автор  
✉️ Альбина Гилязова.
Телеграм @GliazovaAA
