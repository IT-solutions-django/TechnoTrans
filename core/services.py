import os
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont
from PIL import Image as PILImage, ImageDraw, ImageFont
from django.core.files.base import ContentFile 
from io import BytesIO
from django.conf import settings


def convert_image_to_webp(image_field):
    """
    Конвертирует изображение в формат WebP.

    :param image_field: FileField (загруженное изображение)
    :return: InMemoryUploadedFile (сконвертированное изображение)
    """
    output_format = 'WebP'
    if not image_field:
        return None

    image_name = os.path.splitext(os.path.basename(image_field.name))[0].lower()

    img = Image.open(image_field)
    img_io = BytesIO()

    img.save(img_io, format=output_format)
    img_io.seek(0)  

    return InMemoryUploadedFile(
        file=img_io,
        field_name=None,
        name=f"{image_name}.webp",
        content_type=f"image/{output_format.lower()}",
        size=img_io.tell(),
        charset=None,
    )


def add_watermark(image_stream, scale_factor=0.6, transparency=0.35):
    """
    Добавляет логотип в центр изображения.
    :param image_stream: Поток изображения, к которому добавляется водяной знак.
    :param scale_factor: Размер логотипа относительно ширины изображения (по умолчанию 60%).
    :param transparency: Уровень прозрачность логотипа.
    :return: ContentFile с изображением, содержащим логотип.
    """
    image = PILImage.open(image_stream).convert("RGBA")
    if settings.DEBUG: 
        logo_path = os.path.join('static', "images", "logo.png") 
    else:
        logo_path = os.path.join(settings.STATIC_ROOT, "images", "logo.png")
    logo = PILImage.open(logo_path).convert("RGBA")

    logo = logo.copy()
    alpha = logo.split()[3].point(lambda p: int(p * transparency))
    logo.putalpha(alpha)

    logo_width = int(image.width * scale_factor)
    logo_height = int((logo_width / logo.width) * logo.height)
    logo = logo.resize((logo_width, logo_height), PILImage.LANCZOS)
    
    position = (
        (image.width - logo_width) // 2,
        (image.height - logo_height) // 2
    )
    
    watermarked_image = image.copy()
    watermarked_image.paste(logo, position, mask=logo)
    
    output_stream = BytesIO()
    watermarked_image.convert("RGB").save(output_stream, "PNG")
    output_stream.seek(0)
    
    return ContentFile(output_stream.read())