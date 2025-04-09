from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from containers.models import Brand


class CompanyInfo(models.Model): 
    description = models.TextField('Описание', max_length=5000)
    whatsapp_link = models.URLField('Ссылка на WhatsApp', max_length=200, null=True, blank=True)
    telegram_link = models.URLField('Ссылка на Telegram', max_length=200, null=True, blank=True)
    phone = models.CharField('Номер телефона', max_length=20, null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True, max_length=100)

    delivery_info = models.TextField('Доставка (текст)', max_length=1000, null=True, blank=True)
    payment_info = models.TextField('Оплата (текст)', max_length=1000, null=True, blank=True)
    warranty_info_for_new = models.TextField('Гарантия для новых контейнеов (текст)', max_length=1000, null=True, blank=True)
    warranty_info_for_used = models.TextField('Гарантия для б/у контейнеов (текст)', max_length=1000, null=True, blank=True)

    company_full_name = models.CharField('Полное наименование компании', null=True, blank=True, max_length=100, default='ООО "Техно Транс"')
    requisites_file = models.FileField('Реквизиты', null=True, blank=True, upload_to='documentation/requisites/')

    class Meta: 
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'

    def __str__(self):
        return 'Информация о компании'
    
    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls) -> "CompanyInfo":
        instance, created = cls.objects.get_or_create(id=1)
        return instance
    

class CityInfo(models.Model): 
    name = models.CharField('Город', max_length=100) 
    phone = models.CharField('Телефон', max_length=18) 
    email = models.EmailField('Электронная почта', max_length=100) 
    full_address = models.CharField('Адрес', max_length=150)
    whatsapp_link = models.CharField('Ссылка на WhatsApp', max_length=150, null=True, blank=True)
    telegram_link = models.CharField('Ссылка на Telegram', max_length=150, null=True, blank=True)

    class Meta: 
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self) -> str: 
        return f'Филиал {self.name}'
    

class PrivacyPolicy(models.Model): 
    class Meta: 
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls) -> "PrivacyPolicy":
        instance, created = cls.objects.get_or_create(id=1)
        return instance
    
    def __str__(self) -> str: 
        return 'Политика конфиденциальности'


class PrivacyPolicyParagraph(models.Model): 
    title = models.TextField('Заголовок') 
    content = models.TextField('Содержание')
    privacy_policy = models.ForeignKey(verbose_name='Политика конфиденциальности', to=PrivacyPolicy, on_delete=models.CASCADE, related_name='paragraphs')


class DocumentationSection(models.Model): 
    short_name = models.CharField('Название', max_length=50)
    full_name = models.CharField('Полное название', max_length=255) 
    brand = models.ForeignKey(verbose_name='Производитель', to=Brand, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta: 
        verbose_name = 'раздел документации'
        verbose_name_plural = 'Документация'

    def __str__(self) -> str: 
        return f'{self.full_name}'
    

class DocumentationFile(models.Model): 
    file = models.FileField(verbose_name='Файл', upload_to='documentation/')
    doc_section = models.ForeignKey(verbose_name='Раздел документации', to=DocumentationSection, on_delete=models.CASCADE, related_name='files')

    class Meta: 
        verbose_name = 'файл документации'
        verbose_name_plural = 'файлы документации'

    def __str__(self):
        return f'{self.file.name}'
    
    def get_file_name(self): 
        """Возвращает название файла без расширения"""
        print(''.join(os.path.basename(self.file.name).split('.')[:-1]).replace('_', ' '))
        return ''.join(os.path.basename(self.file.name).split('.')[:-1]).replace('_', ' ')


@receiver(post_delete, sender=DocumentationFile)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаляет файл из файловой системы при удалении объекта DocumentationFile
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path) 


class PopularQuestion(models.Model): 
    question = models.CharField('Вопрос', max_length=150)
    answer = models.TextField('Ответ')

    class Meta: 
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Часто задаваемые вопросы'


class Partner(models.Model): 
    company_name = models.CharField('Название компании', max_length=50) 
    company_member = models.CharField('Представитель компании', max_length=100, null=True, blank=True) 
    company_member_image = models.ImageField('Фото представителя компании', upload_to='contacts/partners/members/', null=True, blank=True) 
    logo = models.FileField('Логотип', upload_to='contacts/partners/logo/') 
    quote = models.CharField('Цитата', max_length=150, null=True, blank=True)

    class Meta: 
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'


class WorkStage(models.Model): 
    name = models.CharField('Название', max_length=80) 
    description = models.CharField('Короткое описание', max_length=300) 

    class Meta: 
        verbose_name = 'Этап работы'
        verbose_name_plural = 'Этапы работы'