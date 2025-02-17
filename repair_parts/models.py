from django.db import models
from django.urls import reverse
from core.services import convert_image_to_webp
from containers.models import Brand


class RepairPartCategory(models.Model): 
    name = models.CharField('Название', max_length=50)  

    class Meta: 
        verbose_name = 'Категория запчастей'
        verbose_name_plural = 'Категории запчастей'

    def __str__(self):
        return f'{self.name}'


class RepairPart(models.Model):
    name = models.CharField('Название', max_length=255)
    brand = models.ForeignKey(verbose_name='Производитель', to=Brand, related_name='brand_parts', max_length=255, on_delete=models.CASCADE)
    categories = models.ManyToManyField(verbose_name='Категория', to=RepairPartCategory, related_name='category_parts', blank=True)
    price = models.IntegerField('Цена', default=0)
    old_price = models.IntegerField('Старая цена', default=0)
    is_in_stock = models.BooleanField('В наличии', default=True)
    description = models.TextField('Описание', max_length=2000, default='')
    slug = models.SlugField('Слаг', max_length=500, unique=True, blank=True)

    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

    def __str__(self):
        return f'Запчасть {self.name}'

    def get_absolute_url(self) -> str:
        return reverse('repair_parts:repair_part', args=[self.slug])


class RepairPartImage(models.Model): 
    image = models.ImageField('Картинка', upload_to='containers/') 
    container = models.ForeignKey(verbose_name='Запчасть', to=RepairPart, on_delete=models.CASCADE, related_name='images')

    class Meta: 
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return f'Картинка {self.image}'
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = self.__class__.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.image and old_instance.image.name == self.image.name:
                super().save(*args, **kwargs)
                return

        webp_image = convert_image_to_webp(self.image)
        if webp_image:
            self.image.save(webp_image.name, webp_image, save=False)
        
        super().save(*args, **kwargs)