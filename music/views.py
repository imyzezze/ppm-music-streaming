from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Artist, Album, Song, Playlist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django import forms
from music.models import CustomUser
from django.http import HttpResponseForbidden

# Home - Mostra una panoramica generale
def home(request):
    genres = Genre.objects.all()
    songs = Song.objects.all().order_by('?')[:6]  # Ordine casuale
    albums = Album.objects.all().order_by('?')[:6]  # Ordine casuale
    
    context = {
        'genres': genres,
        'songs': songs,
        'albums': albums,
    }
    return render(request, 'music/home.html', context)

# Lista di tutte le canzoni
def song_list(request):
    songs = Song.objects.all().order_by('title')
    context = {'songs': songs}
    return render(request, 'music/song_list.html', context)

# Dettaglio di una singola canzone
def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    context = {'song': song}
    return render(request, 'music/song_detail.html', context)

# Lista di tutti gli album
def album_list(request):
    albums = Album.objects.all().order_by('title')
    context = {'albums': albums}
    return render(request, 'music/album_list.html', context)

# Dettaglio di un singolo album
def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    songs = album.songs.all()  # Tutte le canzoni di questo album
    context = {'album': album, 'songs': songs}
    return render(request, 'music/album_detail.html', context)

# Lista di tutti i generi
def genre_list(request):
    genres = Genre.objects.all().order_by('name')
    context = {'genres': genres}
    return render(request, 'music/genre_list.html', context)

# Dettaglio di un genere (canzoni di quel genere)
def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    songs = genre.songs.all().order_by('title')  # Tutte le canzoni di questo genere
    context = {'genre': genre, 'songs': songs}
    return render(request, 'music/genre_detail.html', context)

# Form per la registrazione
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match!")
        return cleaned_data
    

# Registrazione
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'listener' 
            user.save()
            login(request, user)
            return redirect('music:home')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'music/register.html', context)


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('music:home')
        else:
            context = {'error': 'Invalid credentials'}
            return render(request, 'music/login.html', context)
    
    return render(request, 'music/login.html')


# Logout
def user_logout(request):
    logout(request)
    return redirect('music:home')


# Curator Dashboard - Solo i curator possono aggiungere canzoni
@login_required(login_url='music:login')
def curator_dashboard(request):
    if request.user.role != 'curator':
        return HttpResponseForbidden("Only curators can access this page")
    
    if request.method == 'POST':
        title = request.POST.get('title')
        album_id = request.POST.get('album')
        genre_id = request.POST.get('genre')
        duration = request.POST.get('duration')
        
        album = Album.objects.get(pk=album_id)
        genre = Genre.objects.get(pk=genre_id) if genre_id else None
        
        Song.objects.create(
            title=title,
            album=album,
            genre=genre,
            duration=int(duration)
        )
        return redirect('music:curator_dashboard')
    
    albums = Album.objects.all()
    genres = Genre.objects.all()
    songs = Song.objects.all().order_by('-created_at')[:10]
    
    context = {
        'albums': albums,
        'genres': genres,
        'songs': songs
    }
    return render(request, 'music/curator_dashboard.html', context)

# Profilo utente
@login_required(login_url='music:login')
def profile(request):
    context = {'user': request.user}
    return render(request, 'music/profile.html', context)

# Lista playlist dell'utente loggato
@login_required(login_url='music:login')
def playlist_list(request):
    # Playlist dell'utente loggato (tutte)
    my_playlists = Playlist.objects.filter(creator=request.user)
    
    # Playlist pubbliche degli altri utenti
    public_playlists = Playlist.objects.filter(is_public=True).exclude(creator=request.user)
    
    # Combina le due
    playlists = my_playlists | public_playlists
    
    context = {'playlists': playlists}
    return render(request, 'music/playlist_list.html', context)


# Dettaglio playlist
@login_required(login_url='music:login')
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    
    # Controlla che solo il creatore possa vederla (se privata)
    if playlist.is_public == False and playlist.creator != request.user:
        return HttpResponseForbidden("You don't have permission to view this playlist")
    
    songs = playlist.songs.all()
    all_songs = Song.objects.all()  # Per aggiungere canzoni
    context = {'playlist': playlist, 'songs': songs, 'all_songs': all_songs}
    return render(request, 'music/playlist_detail.html', context)


# Crea playlist
@login_required(login_url='music:login')
def create_playlist(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        is_public = request.POST.get('is_public') == 'on'
        
        playlist = Playlist.objects.create(
            title=title,
            creator=request.user,
            is_public=is_public
        )
        return redirect('music:playlist_detail', pk=playlist.pk)
    
    return render(request, 'music/create_playlist.html')


# Aggiungi canzone a playlist
@login_required(login_url='music:login')
def add_song_to_playlist(request, pk, song_pk):
    playlist = Playlist.objects.get(pk=pk)
    
    # Solo il creatore può modificare
    if playlist.creator != request.user:
        return HttpResponseForbidden("You don't have permission to edit this playlist")
    
    song = Song.objects.get(pk=song_pk)
    playlist.songs.add(song)
    
    return redirect('music:playlist_detail', pk=pk)


# Rimuovi canzone da playlist
@login_required(login_url='music:login')
def remove_song_from_playlist(request, pk, song_pk):
    playlist = Playlist.objects.get(pk=pk)
    
    # Solo il creatore può modificare
    if playlist.creator != request.user:
        return HttpResponseForbidden("You don't have permission to edit this playlist")
    
    song = Song.objects.get(pk=song_pk)
    playlist.songs.remove(song)
    
    return redirect('music:playlist_detail', pk=pk)