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
    path('competitions/', views.CompetitionListView.as_view(), name='competitions'),
    path('competitions/add', views.CompetitionAddView.as_view(), name='competitionsadd'),
    path('competitions/edit/<int:pk>/', views.CompetitionEditView.as_view(), name='competitionsedit'),
    path('competitions/delete/<int:pk>/', views.CompetitionDeleteView.as_view(), name='competitionsdelete'),
    path('competitions/<int:competition_id>/<int:season_id>/', views.SeasonView.as_view(), name='season')
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^resources/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]