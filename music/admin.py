from django.contrib import admin
from .models import Genre, Artist, Album, Song, Playlist, CustomUser

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date']
    search_fields = ['title', 'artist__name']
    list_filter = ['artist', 'release_date']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'genre', 'duration']
    search_fields = ['title', 'album__title']
    list_filter = ['genre', 'album']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'is_public', 'created_at']
    search_fields = ['title', 'creator__username']
    list_filter = ['is_public', 'created_at']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
    list_filter = ['role']

    