import os
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


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
