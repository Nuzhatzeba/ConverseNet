from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('homepage/<str:user_name>/diary/', views.diary, name='diary'),
    # path('chat/', views.chat, name='chat'),
    path('homepage/<str:user_name>/botchat/', views.botchat, name='botchat'),
    path('', views.loadpage, name='loadpage'),
    path('homepage/<str:user_name>/', views.homepage, name='homepage'),
    path('loadout/', views.loadpage, name='logout'),
    path('homepage/<str:user_name>/profile/', views.profile, name='profile'),
    path('homepage/<str:user_name>/<str:friend_name>/<str:thread_id>/inbox/', views.inbox_page, name='inbox'),
    path('getMessages/<str:thread_id>/', views.getMessages, name='getMessages'),
    path('homepage/<str:user_name>/ResetPassword', views.password_reset, name='password'),
    path('homepage/<str:user_name>/addfriend/', views.addfriend_page, name='addfriend'),




]
