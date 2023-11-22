import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re

#region OBTENER IDs

def get_id_playlist(url_playlist):
    # Verificar si la URL contiene '/playlist/'
    if '/playlist/' in url_playlist:
        # Extraer la ID después de '/playlist/'
        playlist_id = url_playlist.split('/playlist/')[-1].split('?')[0]
        return playlist_id
    else:
        return None

def get_id_artist(url_artista):
    # Verificar si la URL contiene '/artist/'
    if '/artist/' in url_artista:
        # Extraer la ID después de '/artist/'
        artist_id = url_artista.split('/artist/')[-1].split('?')[0]
        return artist_id
    else:
        return None

def get_id_album(url_album):
    # Verificar si la URL contiene '/album/'
    if '/album/' in url_album:
        # Extraer la ID después de '/album/'
        album_id = url_album.split('/album/')[-1].split('?')[0]
        return album_id
    else:
        return None
#endregion

#region ARTISTA

def artistListMaker(playlist): #crea una lista con todos los artistas de la playlist
    artistsList = []
    for item in playlist['items']: # iteramos sobre cada canción de la playlist
        for artist in item['track']['artists']:# iteramos sobre cada artista de la canción
            if artist['id'] not in artistsList:
                artistsList.append(artist['id']) 
    return artistsList

def printArtists(artistsList, sp): #imprimimos todos los artistas de la playlist con el formato: 1) nombre artista
    cont = 1
    for artist_ID in artistsList:
        info_artista = sp.artist(artist_ID)
        print(f'{cont}) {info_artista["name"]}')
        cont += 1

def artistParameter(playlistOriginal, playlist_info, sp): #devuelve una lista con los artistas elegidos por el usuario
    artistsList = artistListMaker(playlistOriginal)
    wantsArtist = str(input('¿Quieres que la playlist sea de un artista en concreto? (y/n): '))  
    if wantsArtist.lower() == 'y':
        print(f'Estos son los artistas de la playlist {playlist_info["name"]}:')
        printArtists(artistsList, sp)
        chosenArtistsNum = str(input('Escribe los números de los artistas que quieres en tu playlist separados por comas: '))
        if chosenArtistsNum: # si la cadena no está vacía
            chosenArtistsNumList = chosenArtistsNum.split(',') # separamos los números de los artistas
            chosenArtists = [] # lista de artistas elegidos (la que se returneará)
            for num in chosenArtistsNumList: # iteramos sobre cada número del artista
                num = int(num.strip())  # Convertir a entero y eliminar espacios en blanco
                if 1 <= num <= len(artistsList): # comprueba si el numero que le has metido está dentro del rango de artistas
                    chosenArtists.append(artistsList[num - 1])
                else:
                    print(f'Error: La posición {num} está fuera de rango. Ignorando esta posición.')
        else:
            print('Error: No se proporcionaron números de artistas. La lista de artistas será nula.')
            chosenArtists = None
    else:
        chosenArtists = None
    return chosenArtists #lista con los ids de los artistas seleccionados

def check_artist(item, chosenArtists): # comprueba si almenos algún artista de la canción está en la lista de artistas elegidos
    bool = False
    for artist in item['track']['artists']:
        if artist['id'] in chosenArtists:
            bool = True
    return bool

#endregion

#region ALBUM

def albumListMaker(playlist): #crea una lista con todos los albumes de la playlist
    albumList = []
    for item in playlist['items']:
        if item['track']['album']['id'] not in albumList and item['track']['album']['album_type'] == 'album': #si el album está en la lista y no es un single
            albumList.append(item['track']['album']['id']) #añadimos el album a la lista
    return albumList

def printAlbums(albumList, sp): # imprime todos los albumes de la playlist con el formato: 1) nombre album
    cont = 1
    for album_ID in albumList:
        info_album = sp.album(album_ID)
        print(f'{cont}) {info_album["name"]}')
        cont += 1

def albumParameter(playlistOriginal, playlist_info, sp):
    albumList = albumListMaker(playlistOriginal)
    wantsAlbum = str(input('¿Quieres que la playlist sea de un álbum en concreto? (y/n): '))
    if wantsAlbum.lower() == 'y':
        print(f'Estos son los álbumes de la playlist {playlist_info["name"]}:')
        printAlbums(albumList, sp) #imprime todos los albumes de la playlist con el formato: 1) nombre album
        chosenAlbumsNum = str(input('Escribe los números de los álbumes que quieres en tu playlist separados por comas: '))
        if chosenAlbumsNum:
            chosenAlbumNumList = chosenAlbumsNum.split(',')
            chosenAlbums = [] # lista de albumes elegidos (la que se returneará)
            for num in chosenAlbumNumList:
                num = int(num.strip())  # Convertir a entero y eliminar espacios en blanco
                if 1 <= num <= len(albumList): # comprueba si el numero que le has metido está dentro del rango de albumes
                    chosenAlbums.append(albumList[num - 1]) #añadimos el album a la lista que se returneará
                else:
                    print(f'Error: La posición {num} está fuera de rango. Ignorando esta posición.')
        else:
            print('Error: No se proporcionaron números de álbumes. La lista de álbumes será nula.')
            chosenAlbums = None
    else:
        chosenAlbums = None
    return chosenAlbums #lista con los ids de los albumes seleccionados

def check_album(item, chosenAlbums): # comprueba si el album de la canción está en la lista de albumes elegidos
    if item['track']['album']['id'] in chosenAlbums:
        return True

#endregion

#region GENERO

def genreListMaker(playlist, sp):
    genresList = []
    for item in playlist['items']:
        track_artist = item['track']['artists'][0]['id']
        info_artista = sp.artist(track_artist)
        for genre in info_artista['genres']:
            if genre not in genresList:
                genresList.append(genre)
    return genresList

def printGenres(genresList):
    cont = 1
    for genre in genresList:
        print(f'{cont}) {genre}')
        cont += 1

def genreParameter(playlistOriginal, playlist_info, sp):
    genreList = genreListMaker(playlistOriginal, sp) # lista con todos los generos de la playlist
    wantsGenre = str(input('¿Quieres que la playlist sea de un género o varios géneros en concreto? (y/n): '))
    if wantsGenre.lower() == 'y':
        print(f'Estos son los géneros de la playlist {playlist_info["name"]}:')
        printGenres(genreListMaker) # imprime todos los generos de la playlist con el formato: 1) nombre genero
        chosenGenresNum = str(input('Escribe los números de los géneros que quieres en tu playlist separados por comas: '))
        if chosenGenresNum:
            chosenGenresNumList = chosenGenresNum.split(',')
            chosenGenres = []
            for num in chosenGenresNumList:
                num = int(num.strip())  # Convertir a entero y eliminar espacios en blanco
                if 1 <= num <= len(genreListMaker): # comprueba si el numero que le has metido está dentro del rango de generos
                    chosenGenres.append(genreListMaker[num - 1])
                else:
                    print(f'Error: La posición {num} está fuera de rango. Ignorando esta posición.')
        else:
            print('Error: No se proporcionaron números de géneros. La lista de géneros será nula.')
            chosenGenres = None
    else:
        chosenGenres = None
    return chosenGenres

def check_genre(item, chosenGenres, sp): # comprueba si alguno de los generos del artista de la cancion está en la lista de generos elegidos
    track_artist = item['track']['artists'][0]['id']
    info_artista = sp.artist(track_artist)
    artist_genres = info_artista['genres']
    for genre in artist_genres:
        if genre in chosenGenres: # si el género está en la lista de géneros de la playlist
            return True
    return False

#endregion

#region AÑO

def yearParameter():
    wantsYear = str(input('Quieres que la playlist sea de un periodo de años en concreto? (y/n): '))
    if wantsYear == 'y':
        initial_year = int(input('Año inicial: '))
        end_year = int(input('Año final: '))
    else:
        initial_year = None
        end_year = None
    return (initial_year, end_year)

def check_year(item, initial_year, end_year): # comprueba que el año del track esté entre los años inicial y final
    if initial_year <= int(item['track']['album']['release_date'].split('-')[0]) <= end_year: # si el año de lanzamiento del album está entre los años inicial y final
        return True
    return False

#endregion

#region POPULARIDAD

def popularityParameter():
    wantsPopularity = str(input('Quieres que la playlist tenga canciones de una popularidad en concreto? (y/n): '))
    if wantsPopularity == 'y':
        try:
            popularity = int(input('Popularidad mínima(0-100): '))
        except ValueError:
            print('Error: La popularidad debe ser un número entre 0 y 100, ahora por tonto te pongo la popularidad en None')
            popularity = None
    else:
        popularity = None
    return popularity

def check_popularity(item, popularity): # si la popularidad es None, no se comprueba
    if item['track']['popularity'] >= popularity:
        return True
    return False

#endregion

#region UNIVERSALES (nombre, descripcion, publica)

def universalParameters(): #name, description, public
    playlist_name = str(input('Nombre de la playlist: '))
    playlist_description = str(input('Descripción de la playlist: '))
    playlist_public = str(input('Quieres que la playlist sea pública? (y/n): '))
    if playlist_public == 'y':
        playlist_public = True
    else:
        playlist_public = False
    return (playlist_name, playlist_description, playlist_public)

#endregion

#region COVER

def coverPlaylist():
    wantsCover = str(input('Quieres que la playlist tenga una portada en concreto? (y/n): '))
    if wantsCover == 'y':
        cover = input('URL de la imagen: ')
    else:
        cover = None
    return cover

def check_url_cover(cover):
    if cover != None:
        try:
            response = requests.head(cover)
            if response.status_code == 200 and response.headers['content-type'].startswith('image'):
                return True
            else:
                return False
        except requests.ConnectionError:
            return False

#endregion

#region PARAMETROS QUE ME VOY A FOLLAR

def parametroDuracionCancionesMax():
    quiereDuracionCanciones = str(input('Quieres que la playlist tenga canciones de una duración máxima en concreto? (y/n): '))
    if quiereDuracionCanciones == 'y':
        duracion_canciones = int(input('Duración en minutos: '))
    else:
        duracion_canciones = None
    return duracion_canciones

def comprobar_duracion_max(track, duracion_canciones_max): # si la duracion maxima es None, no se comprueba
    if track['track']['duration_ms']/60000 <= duracion_canciones_max:
        return True
    return False

def parametroDuracionCancionesMin():
    quiereDuracionCancionesMin = str(input('Quieres que la playlist tenga canciones de una duración mínima en concreto? (y/n): '))
    if quiereDuracionCancionesMin == 'y':
        duracion_canciones_min = int(input('Duración en minutos: '))
    else:
        duracion_canciones_min = None
    return duracion_canciones_min

def comprobar_duracion_min(track, duracion_canciones_min): # si la duracion minima es None, no se comprueba
    if duracion_canciones_min <= track['track']['duration_ms']/60000:
        return True
    return False

def parametroDuracion():
    quiereDuracion = str(input('Quieres que la playlist sea de una duración aproximada? (y/n): '))
    if quiereDuracion == 'y':
        duracion = int(input('Duración en minutos: '))
    else:
        duracion = None
    return duracion

def comprobar_duracion(playlist, duracion): # duracion es la duracion aproximada de la playlist, del metodo parametroDuracion
    if duracion - 5 <= playlist['duration_ms']/60000 <= duracion + 5:
        return True
    return False

def numero_canciones_min():
    quiereNumeroCancionesMin = str(input('Quieres que la playlist tenga un número mínimo de canciones? (y/n): '))
    if quiereNumeroCancionesMin == 'y':
        numero_canciones_min = int(input('Número mínimo de canciones: '))
    else:
        numero_canciones_min = None
    return numero_canciones_min

def comprobar_numero_canciones_min(playlist, numero_canciones_min): # si el numero de canciones minimas es None, no se comprueba
    if numero_canciones_min <= playlist['tracks']['total']:
        return True
    return False

#endregion

#region CREAR PLAYLIST

def extrarCanciones(playlist):
    trackList = []
    for item in playlist['items']:
        trackList.append(item['track']['id'])
    return trackList

def añadirCanciones(listaTracks, nuevaPlaylistID, sp):
    sp.playlist_add_items(nuevaPlaylistID, listaTracks)
    return nuevaPlaylistID

def createPlaylist(dicParameters, sp, playlistOriginal):
    playlist_name = dicParameters['universalParameters'][0]
    playlist_description = dicParameters['universalParameters'][1]
    public = dicParameters['universalParameters'][2]
    new_playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=public, description=playlist_description)
    newTracks = []
    for item in playlistOriginal['items']:
        bool = True
        if dicParameters['artists'] is not None:
            bool = check_artist(item, dicParameters['artists'])
        if dicParameters['genres'] is not None and bool:
            bool = check_genre(item, dicParameters['genres'], sp)
        if dicParameters['years'] != (None, None) and bool:
            bool = check_year(item, dicParameters['years'][0], dicParameters['años'][1])
        if dicParameters['albums'] is not None and bool:
            bool = check_album(item, dicParameters['albums'])
        if dicParameters['popularity'] is not None and bool:
            bool = check_popularity(item, dicParameters['popularity'])
        if bool:
            newTracks.append(item['track']['uri'])
    sp.playlist_add_items(new_playlist['id'], newTracks)
    if dicParameters['cover'] != None and check_url_cover(dicParameters['cover']):
        sp.playlist_upload_cover_image(new_playlist['id'], dicParameters['cover'])
    return new_playlist
#endregion