# Generated by Django 5.1.6 on 2025-02-14 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('containers', '0013_container_old_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип контейнера',
                'verbose_name_plural': 'Типы контейнеров',
            },
        ),
        migrations.CreateModel(
            name='RepairPartCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(max_length=500, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория запчастей',
                'verbose_name_plural': 'Категории запчастей',
            },
        ),
        migrations.CreateModel(
            name='RepairPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('old_price', models.IntegerField(default=0, verbose_name='Старая цена')),
                ('is_in_stock', models.BooleanField(default=True, verbose_name='В наличии')),
                ('description', models.TextField(default='', max_length=2000, verbose_name='Описание')),
                ('slug', models.SlugField(blank=True, max_length=500, unique=True, verbose_name='Слаг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('brand', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='brand_parts', to='containers.brand', verbose_name='Производитель')),
                ('categories', models.ManyToManyField(blank=True, related_name='category_parts', to='repair_parts.repairpartcategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Запчасть',
                'verbose_name_plural': 'Запчасти',
            },
        ),
        migrations.CreateModel(
            name='RepairPartImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='containers/', verbose_name='Картинка')),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='repair_parts.repairpart', verbose_name='Запчасть')),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
            },
        ),
    ]
