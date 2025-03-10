# Generated by Django 5.1.6 on 2025-03-07 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_alter_documentationfile_doc_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Часто задаваемые вопросы',
            },
        ),
    ]
