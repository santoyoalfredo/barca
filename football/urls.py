from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.PlayerListView.as_view(), name='players'),
    path('players/<int:pk>/', views.PlayerView.as_view(), name='player'),
]