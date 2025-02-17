from django.db import models
from django.urls import reverse
from core.services import convert_image_to_webp


class GeneratorCategory(models.Model): 
    name = models.CharField('Название', max_length=50)  

    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'
    

class GeneratorType(models.Model): 
    name = models.CharField('Название', max_length=50) 

    class Meta: 
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    
    def __str__(self):
        return f'{self.name}'
    

class GeneratorPower(models.Model): 
    name = models.CharField('Название', max_length=50) 

    class Meta: 
        verbose_name = 'Мощность'
        verbose_name_plural = 'Мощности'
    
    def __str__(self):
        return f'{self.name}'


class Generator(models.Model): 
    name = models.CharField('Название', max_length=100)
    year = models.SmallIntegerField('Год выпуска') 
    is_in_stock = models.BooleanField('В наличии', default=True)
    generator_type = models.ForeignKey(verbose_name='Тип', to=GeneratorType, on_delete=models.CASCADE, related_name='type_generators')
    categories = models.ManyToManyField(verbose_name='Категория', to=GeneratorCategory, related_name='category_generators', null=True, blank=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=500)
    old_price = models.IntegerField(verbose_name='Старая цена', default=0)
    price = models.IntegerField(verbose_name='Цена', default=0)
    description = models.TextField('Описание', max_length=2000, default='')
    power = models.ForeignKey(verbose_name='Мощность номинальная, квт', to=GeneratorPower, on_delete=models.CASCADE, related_name='power_generators')
    
    class Meta: 
        verbose_name = 'Дизель-генератор'
        verbose_name_plural = 'Дизель-генераторы'

    def __str__(self):
        return f'Генератор {self.name}'
    
    def get_absolute_url(self) -> str: 
        return reverse('generators:generator', args=[self.slug])
    

class GeneratorImage(models.Model): 
    image = models.ImageField('Картинка', upload_to='generators/') 
    generator = models.ForeignKey(verbose_name='Генератор', to=Generator, on_delete=models.CASCADE, related_name='images')

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