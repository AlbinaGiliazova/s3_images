from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid


def process_avatar(image_file):
    # Открыть изображение через Pillow
    image = Image.open(image_file)
    image = image.convert('RGB')  # Для совместимости с JPEG

    # Обрезать по центру до квадрата
    width, height = image.size
    min_side = min(width, height)
    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = left + min_side
    bottom = top + min_side
    image = image.crop((left, top, right, bottom))

    ext = 'jpg'
    file_name = f'{uuid.uuid4().hex}.{ext}'

    # Сжать в JPEG (качество 85, оптимизация)
    output_io = BytesIO()
    image.convert('RGB').save(output_io, format='JPEG', quality=85, optimize=True)
    output_io.seek(0)

    # Вернуть файл, пригодный для Django ImageField
    return InMemoryUploadedFile(
        file=output_io,
        field_name=image_file.field.name,
        name=file_name,
        content_type='image/jpeg',
        size=output_io.getbuffer().nbytes,
        charset=None,
    )
