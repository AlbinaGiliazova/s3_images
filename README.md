# Django: обработка и загрузка аватара с сохранением в S3

Кратко  
Проект автоматически сжимает и обрезает аватары (до квадратной формы), затем сохраняет их в S3-совместимое хранилище.  
Используется Django, Pillow, boto3 и MinIO (локальный S3).
Должен быть установлен Docker.

## Как запустить проект

1. Клонируйте репозиторий  
```
git clone <ссылка на репозиторий>  
cd avatars
```

Переименуйте .env.example в .env

2. Запустите инфраструктуру 
 ```
docker-compose up --build
```

3. Проведите миграции  
```
docker-compose exec django python manage.py migrate
```

4. Запустите тесты  
```
docker-compose exec django python manage.py test tests
```

Ожидается:  
- Ваш аватар уменьшен по размеру  
- Сторона изображения стала квадратной  
- Файл лежит в S3 (MinIO)


S3 (MinIO) доступен по адресу:  
http://localhost:9001  
Логин: minioadmin  
Пароль: miniopassword

## Для регистрации пользователя:
Все запросы начинаются на http://localhost:8000/api/v1/

Отправляете POST-запрос на /api/v1/register/ с полями:
```
    
    {
      "username": "new_user",
      "email": "new_user@example.com",
      "password": "your_password"
    }
```    
Смена пароля пользователя — по /api/v1/change-password/    

Получение JWT-токена (refresh, access):
```
POST /api/v1/token/
Content-Type: application/json

{
  "username": "new_user",
  "password": "your_password"
}
```

При каждом запросе к защищенному эндпоинту передавайте access-токен в заголовке Authorization:

```
Authorization: Bearer <access-токен>
```

Если access-токен истёк — используйте refresh-токен

```
POST /api/v1/token/refresh/
Content-Type: application/json

{
  "refresh": "<ваш refresh токен>"
}

```

Все запросы начинаются на http://localhost:8000/api/v1/

GET /avatars/ — список всех аватаров или фильтрация по user, если добавить ?user=&lt;id&gt;

В полученных адресах картинок замените minio на localhost для просмотра.

GET /avatars/&lt;pk&gt;/ — детальный просмотр любого аватара

GET /upload-avatar/ - получить csrf-токен для загрузки картинки

POST /upload-avatar/ — загрузка только себе (авторизованный пользователь)

Пояснения по архитектуре

- Обработка изображений — через Pillow (resize, crop, сжатие JPEG, PNG)
- Сохранение — через кастомный Storage-класс, основанный на boto3/django-storages
- Хранилище S3 (MinIO) полностью локальное — настройка в docker-compose

## Важные команды

- docker-compose up — старт всего проекта  
- docker-compose exec django python manage.py migrate — миграции  
- docker-compose exec django python manage.py test tests — тесты  
- docker-compose down — остановить проект

## Контакты/автор  
✉️ Альбина Гилязова.
Телеграм @GiliazovaAA
