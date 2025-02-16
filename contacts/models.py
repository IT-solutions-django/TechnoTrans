from django.db import models


class CompanyInfo(models.Model): 
    description = models.TextField('Описание', max_length=5000)

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