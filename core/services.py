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


def add_watermark(image_stream, text="ttrans.pro", font_size=50, position="bottom_left", opacity=200):
    image = PILImage.open(image_stream).convert("RGBA")
    txt_layer = PILImage.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    font_path = os.path.join(settings.STATIC_ROOT, "fonts", "arial.ttf")
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textbbox((0, 0),  text, font)[2:]

    PADDING = 26
    positions = {
        "top_left": (PADDING, PADDING),
        "top_right": (image.width - text_width - PADDING, PADDING),
        "bottom_left": (PADDING, image.height - text_height - PADDING),
        "bottom_right": (image.width - text_width - PADDING, image.height - text_height - PADDING),
        "center": ((image.width - text_width) // 2, (image.height - text_height) // 2)
    }
    text_position = positions.get(position, positions["bottom_left"])
    shadow_offset = (1, 1)
    draw.text((text_position[0] + shadow_offset[0], text_position[1] + shadow_offset[1]), text, font=font, fill=(0, 0, 0, opacity // 2))
    draw.text(text_position, text, font=font, fill=(255, 255, 255, opacity))
    watermarked_image = PILImage.alpha_composite(image, txt_layer)
    
    output_stream = BytesIO()
    watermarked_image.convert("RGB").save(output_stream, "PNG")
    output_stream.seek(0)

    return ContentFile(output_stream.read())