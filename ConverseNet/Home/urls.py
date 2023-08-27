from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('signin/', views.signin, name='signin'),
    path('dairy/', views.dairy, name='dairy'),
    path('', views.loadpage, name='loadpage'),
]
