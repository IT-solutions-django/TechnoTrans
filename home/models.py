from django.db import models
from containers.models import Category


class Request(models.Model): 
    name = models.CharField('Имя', max_length=25)
    phone = models.CharField('Телефон', max_length=18)
    message = models.TextField('Сообщение', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)
    is_closed = models.BooleanField('Обработано', default=False)

    class Meta: 
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    
    def __str__(self) -> str: 
        return f'{"Обработано" if self.is_closed else "Не обработано"}, {self.created_at}, {self.phone}'
    

class ServiceType(models.Model):
    name = models.CharField('Вид обслуживания', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Вид обслуживания'
        verbose_name_plural = 'Виды обслуживания'

    def __str__(self):
        return self.name


class CalculatePriceRequest(models.Model): 
    city = models.CharField('Город', max_length=50)
    phone = models.CharField('Телефон', max_length=18)
    message = models.TextField('Сообщение', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)
    is_closed = models.BooleanField('Обработано', default=False)

    container_type = models.ForeignKey(
        verbose_name='Тип контейнера',
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    service_type = models.ForeignKey(
        verbose_name='Вид обслуживания',
        to=ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta: 
        verbose_name = 'Заявка на расчёт стоимости'
        verbose_name_plural = 'Заявки на расчёт стоимости'
    
    def __str__(self) -> str: 
        return f'{"Обработано" if self.is_closed else "Не обработано"}, {self.created_at}, {self.phone}'
    

class CargoTransportationRequest(models.Model): 
    name = models.CharField('Имя', max_length=100) 
    phone = models.CharField('Телефон', max_length=18) 
    email = models.EmailField('Email', max_length=100)
    inn = models.CharField('ИНН', max_length=12, null=True, blank=True)
    message = models.TextField('Сообщение', max_length=500)
    created_at = models.DateTimeField('Дата и время создания', auto_now_add=True)
    is_closed = models.BooleanField('Обработано', default=False)

    def __str__(self) -> str: 
        return f'{"Обработано" if self.is_closed else "Не обработано"}, {self.created_at}, {self.phone}'
    
    class Meta: 
        verbose_name = 'Заявка на перевозку грузов'
        verbose_name_plural = 'Заявки на перевозки грузов'