from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('create-news/', views.create_news, name='create_news'),

    path('news/<int:id>/', views.news_detail, name='news_detail'),
    
    path('update-news/<int:id>/', views.update_news, name='update_news'),

    path('delete-news/<int:id>/', views.delete_news, name='delete_news'),
    
    path('like/<int:id>/', views.like_news, name='like_news'),
    
    path('api/news/', views.api_news, name='api_news'),
    
    path('category/<int:id>/', views.category_news, name='category_news'),

]