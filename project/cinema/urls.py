from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>', category_view, name='category'),
    # path('cinema/<int:pk>', cinema_view, name='cinema'),
    # path('add_cinema/', add_cinema, name='add_cinema'),

    path('', CinemaListView.as_view(), name='index'),
    path('category/<int:pk>', CinemaListByCategory.as_view(), name='category'),
    path('cinema/<int:pk>', CinemaDetailView.as_view(), name='cinema'),
    path('add_cinema/', NewCinema.as_view(), name='add_cinema'),
    path('cinema/<int:pk>/update', CinemaUpdate.as_view(), name='update'),
    path('cinema/<int:pk>/delete', CinemaDelete.as_view(), name='delete'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register_user, name='register'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('edit_account/', edit_account_view, name='edit_account'),
    path('edit_profile/', edit_profile_view, name='edit_profile')
]