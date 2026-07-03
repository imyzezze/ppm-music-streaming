from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# 1. Genre: genere musicale
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

# 2. Artist: artista musicale 
class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

# 3. Album: album musicale (ForeignKey a Artist)
class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField(blank=True, null=True)
    cover = models.ImageField(upload_to='albums/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    class Meta:
        ordering = ['-release_date']
        unique_together = ('title', 'artist')  # Stessa canzone con artista diverso va bene

# 4. Song: canzone (ForeignKey a Album e Genre)
class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')
    duration = models.IntegerField()  # Durata in secondi
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.album.artist.name}"
    
    class Meta:
        ordering = ['album', 'title']
        unique_together = ('title', 'album')  # Stesso album non può avere due canzoni con lo stesso titolo 

# 5. Playlist: lista di canzoni creata da un utente (ManyToMany a Song, ForeignKey a User)
class Playlist(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    is_public = models.BooleanField(default=False)  # Pubblica o privata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.creator.username}"
    
    class Meta:
        ordering = ['-created_at']


from django.contrib.auth.models import AbstractUser

# Custom User Model con ruoli
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('listener', 'Listener'),
        ('curator', 'Curator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='listener')
    
    def __str__(self):
        return f"{self.username} ({self.role})"