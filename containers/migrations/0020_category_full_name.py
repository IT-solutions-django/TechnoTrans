# Generated by Django 5.1.6 on 2025-03-11 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0019_container_with_nds'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название в шапке сайта'),
        ),
    ]
