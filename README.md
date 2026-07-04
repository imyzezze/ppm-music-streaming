# Music Streaming Service

**Student:** Imane Zeroual
**University:** Università degli Studi di Firenze  
**Course:** Progettazione e Produzione Multimediale

## Project Type

Full-Stack Web Application

## Framework

Django 5.2.15 (Python 3.10)

## Description

Music Streaming Service is a Django web application where users can browse music, create personal playlists, and manage their library. The app features user authentication, role-based access control (Listener vs Curator), and a dark-themed interface inspired by Spotify.

## Features

### Listener (Default Role)
- Browse songs, albums, artists, and genres
- Create and manage personal playlists (private or public)
- Add and remove songs from own playlists
- View public playlists from other users
- Cannot modify other users' playlists
- User profile page

### Curator (Special Role)
- All Listener features
- Access to Curator Dashboard
- Add new songs to the music library
- Manage song metadata (album, genre, duration)

### Admin (Superuser)
- Full Django Admin access
- Manage all content
- Assign and change user roles
- Database management

## Installation

### On Mac/Linux
```bash
git clone https://github.com/imyzezze/ppm-music-streaming.git
cd ppm-music-streaming
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### On Windows
```bash
git clone https://github.com/imyzezze/ppm-music-streaming.git
cd ppm-music-streaming
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Access the app at http://127.0.0.1:8000/

## Database

File: `db.sqlite3`

Contains demo data:
- 7 genres
- 9 artists
- 14 albums
- 34 songs
- 4 user accounts

## Demo Accounts

| Username | Password | Role |
|----------|----------|------|
| admin | admin12345 | Admin |
| user | user12345 | Listener |
| user2 | user23456 | Listener |
| curator_demo | curator12345 | Curator |

## Testing Scenario

### Test 1: Browse Music
1. Go to http://127.0.0.1:8000/
2. Click "Songs" - songs are ordered alphabetically
3. Click on a song - view song details
4. Go back, click "Albums" - explore albums
5. Click an album - see all songs in that album

### Test 2: Create and Manage Playlist
1. Click "Register" - create new account (auto-assigned as Listener)
2. Login with your new account
3. Click "Playlists" - click "Create Playlist"
4. Name it "My Favorites" and check "Make this playlist public"
5. Click "Create"
6. Add songs to your playlist
7. Try removing a song - it disappears from the playlist

### Test 3: Test Playlist Permissions
1. Login as `user / user12345`
2. Go to Playlists - note the songs
3. Logout and login as `user2 / user23456`
4. Go to Playlists - you can see user's public playlist
5. Click on it - you can view but there's no "Remove" button
6. Only the creator can modify their own playlists
7. **Result:** Permissions work correctly. Each user can only modify their own playlists.

### Test 4: Curator Dashboard
1. Login as `curator_demo / curator12345`
2. Notice "Curator" link appears in navbar (not visible for listeners)
3. Click "Curator" - see Curator Dashboard
4. Fill the form with: title, album, genre, duration
5. Click "Add Song"
6. Song appears in "Recently Added Songs"
7. **Result:** Only curators can access this dashboard and add songs.

### Test 5: Admin Panel
1. Login as `admin / admin12345`
2. Go to http://127.0.0.1:8000/admin/
3. Manage Songs, Albums, Artists, Genres, Playlists, Users
4. View all users and their roles
5. **Result:** Admin has full control.

## Tech Stack

- **Backend:** Django 5.2.15, Python 3.10
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5.3.0
- **Styling:** Custom CSS, Montserrat font

## Design & UI

- **Theme:** Dark mode (#0f0f0f background, #1a1a2e cards)
- **Primary Color:** Blue (#2563eb)
- **Font:** Montserrat (Google Fonts)
- **Framework:** Bootstrap 5.3.0
- **Responsive:** Mobile-friendly

## Key Features

- User Authentication (Login/Register/Logout)
- Role-Based Access Control (Listener/Curator/Admin)
- Custom User Model with Role Field
- Playlist Management (Create, Read, Update, Delete)
- Permission Checking (Users can't modify others' playlists)
- Curator Dashboard (Add songs to library)
- Responsive Dark Theme UI with Bootstrap
- Django Admin Panel
- Pre-populated Database with Demo Data

## Security & Permissions

- Password hashing with Django
- @login_required decorator on protected views
- Role-based access control
- Private playlists only accessible by creator
- HttpResponseForbidden for unauthorized access

## Online Deployment

https://imyzezze.pythonanywhere.com

## Notes for Professor

- The application is fully functional and ready for testing
- All demo accounts are pre-configured with correct permissions
- The database includes sample data for immediate testing
- Permissions are working correctly - users cannot modify others' playlists
- The Curator role successfully demonstrates role-based access control
- All features from the assignment have been implemented
- Testing scenario is provided above for easy verification


**Created:** July 2026
**Repository:** https://github.com/imyzezze/ppm-music-streaming
