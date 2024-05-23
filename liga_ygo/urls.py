from django.contrib import admin
from django.urls import path
from liga import views  # Importa as views do app 'liga'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tournament_day/', views.tournament_day, name='tournament_day'),
    path('player_registration/', views.player_registration, name='player_registration'),
    path('tournament/register/', views.register_tournament, name='register_tournament'),
    path('tournaments/', views.list_tournaments, name='list_tournaments'),
    path('ranking/', views.view_ranking, name='view_ranking'),
    path('tournament/<int:tournament_id>/results/', views.tournament_results, name='tournament_results'),
    path('export/csv/', views.export_rankings_csv, name='export_rankings_csv'),
    path('deck/register/', views.deck_registration, name='deck_registration'),
    path('decks/', views.view_decks, name='view_decks'),
    path('ver-jogadores/', views.view_players, name='view_players'),
    path('decks/', views.show_decks, name='show_decks'),

]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)