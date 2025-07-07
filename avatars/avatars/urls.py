from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        's3_avatars/',
        include(('s3_avatars.urls', 's3_avatars'), namespace='s3_avatars'),
    ),
]
