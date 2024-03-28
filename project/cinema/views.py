from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Cinema, Comment, Profile
from .forms import CinemaForm, LoginForm, RegisterForm, CommentForm, EditAccountForm, EditProfileForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib import messages


# Create your views here.


# def index(request):
#     cinemas = Cinema.objects.all()  # Из БД получаем все фильмы
#     context = {
#         'title': 'Главная страница: KinoMonstr',
#         'cinemas': cinemas
#     }
#     return render(request, 'cinema/index.html', context)

class CinemaListView(ListView):
    model = Cinema  # С какой модели получаю
    template_name = 'cinema/index.html'  # Для какой страницы класс
    context_object_name = 'cinemas'  # Под каким именем будим получать все фильмы
    extra_context = {
        'title': 'Главная страница: KinoMonstr'
    }


# ----------------------------------------------------------------------------
# Функция для получения фильмов по категории на главной странице
# def category_view(request, pk):
#     cinemas = Cinema.objects.filter(category_id=pk)
#     category = Category.objects.get(pk=pk)
#     context = {
#         'title': f'Кинофильмы: {category.title}',
#         'cinemas': cinemas
#     }
#
#     return render(request, 'cinema/index.html', context)


class CinemaListByCategory(CinemaListView):

    # Метод классы которым получаем фильмы по категориям
    def get_queryset(self):
        cinemas = Cinema.objects.filter(category_id=self.kwargs['pk'])
        return cinemas

    # Метод при помощи которого можно отправлять в контексте что ещё на страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Кинофильмы: {category.title}'
        return context


# ----------------------------------------------------------------------------
# Функция для страницы фильма
# def cinema_view(request, pk):
#     cinema = Cinema.objects.get(pk=pk)
#     cinemas = Cinema.objects.all()[::-1][:3]
#     context = {
#         'title': f'Кинофильм: {cinema.title}',
#         'cinema': cinema,
#         'cinemas': cinemas
#     }
#
#     return render(request, 'cinema/cinema_detail.html', context)


class CinemaDetailView(DetailView):
    model = Cinema
    context_object_name = 'cinema'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cinema = Cinema.objects.get(pk=self.kwargs['pk'])
        cinema.views += 1
        cinema.save()
        cinemas = Cinema.objects.all()[::-1][:3]
        context['title'] = f'Кинофильм: {cinema.title}'
        context['cinemas'] = cinemas
        context['comments'] = Comment.objects.filter(cinema=cinema)

        if self.request.user.is_authenticated:  # Если пользователь Авторизован то будит видеть форму комментариев
            context['form'] = CommentForm()
        return context


# ----------------------------------------------------------------------------
# Функция для добавления фильма на сайт
# def add_cinema(request):
#     if request.method == 'POST':
#         form = CinemaForm(request.POST, request.FILES)  # Говорим что получаем из запроса
#         if form.is_valid():
#             cinema = Cinema.objects.create(**form.cleaned_data)
#             cinema.save()
#             return redirect('cinema', cinema.pk)
#     else:
#         form = CinemaForm()
#
#     context = {
#         'title': 'Добавить кинофиль',
#         'form': form
#     }
#
#     return render(request, 'cinema/add_cinema.html', context)


class NewCinema(CreateView):
    form_class = CinemaForm
    template_name = 'cinema/add_cinema.html'
    extra_context = {
        'title': 'Добавить кинофильм'
    }

    # Метод для добавления автора кинофильму
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CinemaUpdate(UpdateView):
    model = Cinema
    form_class = CinemaForm
    template_name = 'cinema/add_cinema.html'
    extra_context = {
        'title': 'Изменить кинофильм'
    }


# Класс для удаления кинофильма
class CinemaDelete(DeleteView):
    model = Cinema
    context_object_name = 'cinema'
    success_url = reverse_lazy('index')


# Функция для входа в Акааунт
def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)  # Получаем данные введённые пользовтаелем
        if login_form.is_valid():
            user = login_form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Успешный вход в Аккаунт')
                return redirect('index')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Не верный логин или пароль')
            return redirect('login')

    else:
        login_form = LoginForm()  # Здесь поставим класс Формы Логина

    context = {
        'title': 'Войти в Аккаунт',
        'login_form': login_form
    }
    if not request.user.is_authenticated:  # Если пользователь не Авторизован он может перейти на Логин
        return render(request, 'cinema/login.html', context)
    else:
        return redirect('index')


def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из Аккаунта')
    return redirect('index')


# Функция для регистрации
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Должен создаваться профиль пользователю после регистрации
            profile = Profile.objects.create(user=user)
            profile.save()

            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('register')

    else:
        form = RegisterForm()  # Форма для регистрации

    context = {
        'title': 'Регистрация',
        'form': form
    }

    if not request.user.is_authenticated:
        return render(request, 'cinema/register.html', context)
    else:
        return redirect('index')


# Функция для сохранения комментария
def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.cinema = Cinema.objects.get(pk=pk)  # Указали на какой фильм комент
        comment.user = request.user  # Какой пользователь
        comment.save()
        messages.success(request, 'Ваш комментарий оставлен')
        return redirect('cinema', pk)


# Фнукция для страницы профиля
def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    cinemas = Cinema.objects.filter(author_id=pk)
    most_viewed = cinemas.order_by('-views')[:1][0]
    recent_cinema = cinemas.order_by('-created_at')[:1][0]
    if most_viewed.views == 0:
        most_viewed = 'НЕТ популярныйх фильмов'

    context = {
        'title': f'Профиль: {request.user.username}',
        'profile': profile,
        'most_viewed': most_viewed,
        'recent_cinema': recent_cinema
    }

    return render(request, 'cinema/profile.html', context)


# Функция для страницы изменения аккаунта пользователя
def edit_account_view(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные Аккаунта изменены')
            return redirect('profile', request.user.pk)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('change')

    else:
        form = EditAccountForm(instance=request.user)

    context = {
        'title': f'Измененние Аккаунта: {request.user.username}',
        'form': form
    }

    return render(request, 'cinema/change.html', context)




def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные Профиля изменены')
            return redirect('profile', request.user.pk)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('change')

    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        'title': f'Измененние Профиля: {request.user.username}',
        'form': form
    }

    return render(request, 'cinema/change.html', context)











