from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dairy/', views.dairy, name='dairy'),
    path('chat/', views.chat, name='chat'),
    path('botchat/', views.botchat, name='botchat'),
    path('', views.loadpage, name='loadpage'),
]
