from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.all_blogs, name='all_blogs'),
    path('myblogs/', views.my_blogs, name='my_blogs'),
    path('create/', views.create_blog, name='create_blog'),
    path('edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
]
