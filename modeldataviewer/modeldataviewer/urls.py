from django.contrib import admin
from django.urls import path, re_path
from viewer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    re_path(r'^callback/oauth/$', views.oauth, name='oauth'),
    path('Users/', views.Users, name='Users'),
]
