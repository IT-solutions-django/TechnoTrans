# Generated by Django 5.1.6 on 2025-02-07 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0002_category_alter_containermodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(default='', max_length=500, verbose_name='Описание'),
            preserve_default=False,
        ),
    ]
