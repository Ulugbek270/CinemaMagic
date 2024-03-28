# Generated by Django 4.2.5 on 2023-10-28 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0004_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Фото профиля')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона')),
                ('about_user', models.CharField(blank=True, max_length=100, null=True, verbose_name='О себе')),
                ('publisher', models.BooleanField(default=True, verbose_name='Прво на добавление фильма')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
