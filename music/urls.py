from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.song_list, name='song_list'),
    path('songs/<int:pk>/', views.song_detail, name='song_detail'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<int:pk>/', views.album_detail, name='album_detail'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genres/<int:pk>/', views.genre_detail, name='genre_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('curator/', views.curator_dashboard, name='curator_dashboard'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/<int:pk>/add-song/<int:song_pk>/', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('playlists/<int:pk>/remove-song/<int:song_pk>/', views.remove_song_from_playlist, name='remove_song_from_playlist'),
]
