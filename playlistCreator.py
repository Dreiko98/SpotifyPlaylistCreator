import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistCreatorMetods import *

# Coloca aquí tus credenciales
client_id = 'cc2ece12ff0840e68932c542a3870c46'
client_secret = '85fe48dc89d2469aa8a39ca57838e7e6'
redirect_uri = 'http://localhost:8888/callback'

# Configuración de autenticación de usuario
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-private'))

# Nombre de usuario de Spotify
username = 'germanmallo44'
print(f'bienvenido a playlist creator, {username}')

# recibir playlist original
url_playlist = 'https://open.spotify.com/playlist/6xTntSEzzkk1m5xu99qu5o?si=118c4332e812477d'
id_playlist = get_id_playlist(url_playlist)
playlistOriginal = sp.playlist_tracks(id_playlist, limit = 100) # playlist por paginas de 100 canciones
playlist_info = sp.playlist(id_playlist)
print(f'La playlist original es: {playlist_info["name"]}')

# elegir parámetros para la playlist
print('Cargando, no toques nada niño rata')
print('Ingresa los parámetros para la playlist nueva')
parameters = {}

# ARTISTAS
chosenArtists = artistParameter(playlistOriginal, playlist_info, sp)
parameters['artists'] = chosenArtists
artists_name = []
if chosenArtists != None and chosenArtists: # si se eligieron artistas
    for artist in chosenArtists:
        artist_info = sp.artist(artist)
        artist_name = artist_info['name']
        artists_name.append(artist_name)
    print(f'Artistas elegidos: {artists_name}')
else:
    chosenArtists = None
    print('No se eligieron artistas')

# ALBUM
chosenAlbums = albumParameter(playlistOriginal, playlist_info, sp)
parameters['albums'] = chosenAlbums
albums_name = []
if chosenAlbums != None and chosenAlbums:
    for album in chosenAlbums:
        album_info = sp.album(album)
        album_name = album_info['name']
        albums_name.append(album_name)
    print(f'Albumes elegidos: {albums_name}')
else:
    chosenAlbums = None
    print('No se eligieron albumes')

# AÑO
years = yearParameter()
parameters['years'] = years
print(f'Intervaflo de años elegido: {years}')

# POPULARIDAD
popularity = popularityParameter()
parameters['popularity'] = popularity
print(f'Popularidad mínima elegida: {popularity}')

# COVER
cover_url = coverPlaylist()
parameters['cover'] = cover_url
print(f'Cover elegido: {cover_url}')

# CREAR PLAYLIST

new_playlist = createPlaylist(parameters, sp, playlistOriginal)