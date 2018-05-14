from django.urls import path
from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.PlayerListView.as_view(), name='players'),
    path('players/<int:pk>/', views.PlayerView.as_view(), name='player'),
    path('players/add/', views.PlayerAddView.as_view(), name='playersadd'),
    path('players/edit/<int:pk>/', views.PlayerEditView.as_view(), name='playersedit'),
    path('players/delete/<int:pk>/', views.PlayerDeleteView.as_view(), name='playersdelete'),
    path('competitions/', views.CompetitionListView.as_view(), name='competitions'),
    path('competitions/add/', views.CompetitionAddView.as_view(), name='competitionsadd'),
    path('competitions/edit/<int:pk>/', views.CompetitionEditView.as_view(), name='competitionsedit'),
    path('competitions/delete/<int:pk>/', views.CompetitionDeleteView.as_view(), name='competitionsdelete'),
    path('competitions/<int:competition_id>/<int:pk>/', views.SeasonView.as_view(), name='season'),
    path('competitions/<int:competition_id>/add/', views.SeasonAddView.as_view(), name='seasonsadd'),
    path('competitions/<int:competition_id>/edit/<int:pk>', views.SeasonEditView.as_view(), name='seasonsedit'),
    path('competitions/<int:competition_id>/delete/<int:pk>', views.SeasonDeleteView.as_view(), name='seasonsdelete')
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^resources/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]