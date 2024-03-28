from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

    # Умная ссылка
    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



#   null=True, blank=True, - делаем поле не обязательным для заполнения
class Cinema(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название фильма')
    context = models.TextField(verbose_name='Описание фильма')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    video = models.CharField(max_length=255, verbose_name='Ссылка видео', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор')

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('cinema', kwargs={'pk': self.pk})

    def get_photo_cinema(self):
        try:
            return self.photo.url
        except:
            return 'https://forum.endeavouros.com/uploads/default/original/2X/a/ab62dc01f05c1ee26d3c613bc4db6cd953a44b9b.png'

    class Meta:
        verbose_name = 'Кинофильм'
        verbose_name_plural = 'Кинофильмы'


# Моделька комментариев
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Коментатор')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Фильм')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата коментария')


    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

# Моделька профиля
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фото профиля')
    phone_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер телефона')
    about_user = models.CharField(max_length=100, blank=True, null=True, verbose_name='О себе')
    publisher = models.BooleanField(default=True, verbose_name='Прво на добавление фильма')

    def __str__(self):
        return self.user.username

    # Метод модели для получения фото пользователя
    def get_photo_user(self):
        try:
            return self.photo.url
        except:
            return 'https://bootdey.com/img/Content/avatar/avatar7.png'


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



