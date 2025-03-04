from django.db import models
from django.urls import reverse
from core.services import convert_image_to_webp, add_watermark


class Category(models.Model): 
    name = models.CharField('Название', max_length=50)  
    description = models.TextField('Описание', max_length=500)

    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class ContainerType(models.Model): 
    name = models.CharField('Название', max_length=50) 

    class Meta: 
        verbose_name = 'Тип контейнера'
        verbose_name_plural = 'Типы контейнеров'
    
    def __str__(self):
        return f'{self.name}'
    

class Brand(models.Model): 
    name = models.CharField('Название', max_length=50)
    image = models.ImageField('Логотип', upload_to='brands/') 

    class Meta: 
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
    
    def __str__(self):
        return f'{self.name}'
    

class ContainerModel(models.Model): 
    name = models.CharField('Название', max_length=50) 

    class Meta: 
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
    
    def __str__(self):
        return f'{self.name}'


class Container(models.Model): 
    name = models.CharField('Название', max_length=100)
    model = models.ForeignKey(verbose_name='Модель', to=ContainerModel, on_delete=models.CASCADE, related_name='model_containers')
    year = models.SmallIntegerField('Год выпуска') 
    is_in_stock = models.BooleanField('В наличии', default=True)
    container_type = models.ForeignKey(verbose_name='Тип', to=ContainerType, on_delete=models.CASCADE, related_name='type_containers')
    brand = models.ForeignKey(verbose_name='Бренд', to=Brand, on_delete=models.CASCADE)
    categories = models.ManyToManyField(verbose_name='Категория', to=Category, related_name='category_containers', null=True, blank=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=500)
    old_price = models.IntegerField(verbose_name='Старая цена', default=0)
    price = models.IntegerField(verbose_name='Цена', default=0)
    description = models.TextField('Описание', max_length=2000, default='')

    length_outer = models.SmallIntegerField('Длина внешняя', null=True, blank=True)
    width_outer = models.SmallIntegerField('Ширина внешняя', null=True, blank=True)
    height_outer = models.SmallIntegerField('Высота внешняя', null=True, blank=True)
    length_inner = models.SmallIntegerField('Длина внутренняя', null=True, blank=True)
    width_inner = models.SmallIntegerField('Ширина внутренняя', null=True, blank=True)
    height_inner = models.SmallIntegerField('Высота внутренняя', null=True, blank=True)

    max_weight_gross = models.SmallIntegerField('Макс. масса брутто', null=True, blank=True)
    tare_weight = models.SmallIntegerField('Вес тары', null=True, blank=True)
    max_load = models.SmallIntegerField('Максимальная загрузка', null=True, blank=True)
    
    door_width = models.SmallIntegerField('Ширина дверного проёма', null=True, blank=True)
    doorh_height = models.SmallIntegerField('Высота дверного проёма', null=True, blank=True)
    
    class Meta: 
        verbose_name = 'Контейнер'
        verbose_name_plural = 'Контейнеры'

    def __str__(self):
        return f'Контейнер {self.name}'
    
    def get_absolute_url(self) -> str: 
        return reverse('containers:container', args=[self.slug])


class ContainerImage(models.Model): 
    image = models.ImageField('Картинка', upload_to='containers/') 
    container = models.ForeignKey(verbose_name='Контейнер', to=Container, on_delete=models.CASCADE, related_name='images')

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

        watermarked_image = add_watermark(
            image_stream=webp_image
        )

        if watermarked_image:
            self.image.save(webp_image.name, watermarked_image, save=False)
        
        super().save(*args, **kwargs)