# Generated by Django 5.1.6 on 2025-02-16 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_calculatepricerequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Вид обслуживания')),
            ],
            options={
                'verbose_name': 'Вид обслуживания',
                'verbose_name_plural': 'Виды обслуживания',
            },
        ),
    ]
