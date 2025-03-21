# Generated by Django 5.1.6 on 2025-03-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0017_workstage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Город')),
                ('phone', models.CharField(max_length=18, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=100, verbose_name='Электронная почта')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
    ]
