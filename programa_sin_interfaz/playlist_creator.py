import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistCreatorMetods import *
import os


def spotify_creator():

    REDIRECT_URI = 'http://localhost:5000/redirect'
    SCOPE = 'user-library-read playlist-modify-public playlist-modify-private'

    cache_file = '.cache' # o '.cache-username' con tu nombre de usuario de Spotify
    if os.path.exists(cache_file):
        os.remove(cache_file)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENT_ID",
                                                client_secret="CLIENT_SECRET",
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE,
                                                cache_path=None, # Evitar el uso de archivo de caché
                                                show_dialog=True)) # Forzar cuadro de diálogo

    url_playlist = input('Ingresa la URL de la playlist original (tiene que ser publica o de tu pertenencia): ')
    id_playlist = get_id_playlist(url_playlist)
    playlistOriginal = sp.playlist_tracks(id_playlist, limit = 100) # playlist por paginas de 100 canciones
    playlist_info = sp.playlist(id_playlist)
    print(f'La playlist original es: {playlist_info["name"]}')

    # elegir parámetros para la playlist
    print('Cargando...')
    print('Ingresa los parámetros para la playlist nueva')
    parameters = {}

    # ARTISTAS
    chosenArtists = artistParameter(playlistOriginal, playlist_info, sp) # lista de artistas elegidos, los elementos son los id de los artistas
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
    print(f'Intervalo de años elegido: {years}')

    # COVER
    cover_url = coverPlaylist()
    parameters['cover'] = cover_url
    print(f'Cover elegido: {cover_url}')    
    #endregion

    # CREAR PLAYLIST
    new_playlist = createPlaylist(parameters, sp, playlistOriginal)
    return (f'Playlist creada exitosamente, ve a tu cuenta de Spotify para verla')


if __name__ == "__main__":
    spotify_creator()