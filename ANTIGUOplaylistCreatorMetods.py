import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re

#region METODOS PARA OBTENER ID DE LA PLAYLIST, ARTISTA Y ALBUM

def obtener_id_playlist(url_playlist):
    # Verificar si la URL contiene '/playlist/'
    if '/playlist/' in url_playlist:
        # Extraer la ID después de '/playlist/'
        playlist_id = url_playlist.split('/playlist/')[-1].split('?')[0]
        return playlist_id
    else:
        return None

def obtener_id_artista(url_artista):
    # Verificar si la URL contiene '/artist/'
    if '/artist/' in url_artista:
        # Extraer la ID después de '/artist/'
        artist_id = url_artista.split('/artist/')[-1].split('?')[0]
        return artist_id
    else:
        return None

def obtener_id_album(url_album):
    # Verificar si la URL contiene '/album/'
    if '/album/' in url_album:
        # Extraer la ID después de '/album/'
        album_id = url_album.split('/album/')[-1].split('?')[0]
        return album_id
    else:
        return None
#endregion

# region METODOS PARA OBTENER LISTAS DE ARTISTAS, ALBUMES Y GENEROS

def listaGeneros(playlist, sp):
    listGenres = []
    for track in playlist['items']:
        artista = track['track']['artists'][0]['id']
        info_artista = sp.artist(artista)
        for genre in info_artista['genres']:
            if genre not in listGenres:
                listGenres.append(genre)
    return listGenres

def listaArtistas(playlist):
    listaArtistas = []
    for track in playlist['items']:
        if track['track']['artists'][0]['id'] not in listaArtistas:
            listaArtistas.append(track['track']['artists'][0]['id'])
    return listaArtistas

def listaAlbumes(playlist):
    listaAlbumes = []
    for track in playlist['items']:
        if track['track']['album']['id'] not in listaAlbumes and track['track']['album']['album_type'] == 'album':
            listaAlbumes.append(track['track']['album']['id'])
    return listaAlbumes
#endregion

# region METODOS PARA IMPRIMIR LISTAS DE ARTISTAS, ALBUMES Y GENEROS

def imprimirAlbumes(listaAlbumes, sp):
    cont = 1
    for album_ID in listaAlbumes:
        info_album = sp.album(album_ID)
        print(f'{cont}) {info_album["name"]}')
        cont += 1

def imprimirArtistas(listaArtistas, sp):
    cont = 1
    for artist_ID in listaArtistas:
        info_artista = sp.artist(artist_ID)
        print(f'{cont}) {info_artista["name"]}')
        cont += 1

def imprimirGeneros(listaGeneros):
    cont = 1
    for genre in listaGeneros:
        print(f'{cont}) {genre}')
        cont += 1
#endregion

# region PARAMETROS DE LAS CANCIONES DE LA PLAYLIST

def parametroArtista(playlistOriginal, playlist_info, sp):
    artistsList = listaArtistas(playlistOriginal)
    quiereArtista = str(input('¿Quieres que la playlist sea de un artista en concreto? (y/n): '))
    
    if quiereArtista.lower() == 'y':
        print(f'Estos son los artistas de la playlist {playlist_info["name"]}:')
        imprimirArtistas(artistsList, sp)
        
        artistas_elegidos = str(input('Escribe los números de los artistas que quieres en tu playlist separados por comas: '))

        if artistas_elegidos:
            pos_artistas = artistas_elegidos.split(',')
            artistas = []

            for pos in pos_artistas:
                pos = int(pos.strip())  # Convertir a entero y eliminar espacios en blanco
                if 1 <= pos <= len(artistsList):
                    artistas.append(artistsList[pos - 1])
                else:
                    print(f'Error: La posición {pos} está fuera de rango. Ignorando esta posición.')

        else:
            print('Error: No se proporcionaron números de artistas. La lista de artistas será nula.')
            artistas = None

    else:
        artistas = None

    return artistas

def parametroGenero(playlistOriginal, playlist_info, sp):
    genreList = listaGeneros(playlistOriginal, sp)
    quiereGenero = str(input('¿Quieres que la playlist sea de un género o varios géneros en concreto? (y/n): '))
    
    if quiereGenero.lower() == 'y':
        print(f'Estos son los géneros de la playlist {playlist_info["name"]}:')
        imprimirGeneros(genreList)
        
        generos_elegidos = str(input('Escribe los números de los géneros que quieres en tu playlist separados por comas: '))

        if generos_elegidos:
            pos_generos = generos_elegidos.split(',')
            generos = []

            for pos in pos_generos:
                pos = int(pos.strip())  # Convertir a entero y eliminar espacios en blanco
                if 1 <= pos <= len(genreList):
                    generos.append(genreList[pos - 1])
                else:
                    print(f'Error: La posición {pos} está fuera de rango. Ignorando esta posición.')

        else:
            print('Error: No se proporcionaron números de géneros. La lista de géneros será nula.')
            generos = None

    else:
        generos = None

    return generos

def parametroAlbum(playlistOriginal, playlist_info, sp):
    albumList = listaAlbumes(playlistOriginal)
    quiereAlbum = str(input('¿Quieres que la playlist sea de un álbum en concreto? (y/n): '))
    
    if quiereAlbum.lower() == 'y':
        print(f'Estos son los álbumes de la playlist {playlist_info["name"]}:')
        imprimirAlbumes(albumList, sp)
        
        albumes_elegidos = str(input('Escribe los números de los álbumes que quieres en tu playlist separados por comas: '))

        if albumes_elegidos:
            pos_albumes = albumes_elegidos.split(',')
            albumes = []

            for pos in pos_albumes:
                pos = int(pos.strip())  # Convertir a entero y eliminar espacios en blanco
                if 1 <= pos <= len(albumList):
                    albumes.append(albumList[pos - 1])
                else:
                    print(f'Error: La posición {pos} está fuera de rango. Ignorando esta posición.')

        else:
            print('Error: No se proporcionaron números de álbumes. La lista de álbumes será nula.')
            albumes = None

    else:
        albumes = None

    return albumes

def parametroAnio():
    quiereAnio = str(input('Quieres que la playlist sea de un periodo de años en concreto? (y/n): '))
    if quiereAnio == 'y':
        anio_inicial = int(input('Año inicial: '))
        anio_final = int(input('Año final: '))
    else:
        anio_inicial = None
        anio_final = None
    return (anio_inicial, anio_final)

def parametroDuracionCancionesMax():
    quiereDuracionCanciones = str(input('Quieres que la playlist tenga canciones de una duración máxima en concreto? (y/n): '))
    if quiereDuracionCanciones == 'y':
        duracion_canciones = int(input('Duración en minutos: '))
    else:
        duracion_canciones = None
    return duracion_canciones

def parametroDuracionCancionesMin():
    quiereDuracionCancionesMin = str(input('Quieres que la playlist tenga canciones de una duración mínima en concreto? (y/n): '))
    if quiereDuracionCancionesMin == 'y':
        duracion_canciones_min = int(input('Duración en minutos: '))
    else:
        duracion_canciones_min = None
    return duracion_canciones_min

def parametroPopularidad():
    quierePopularidad = str(input('Quieres que la playlist tenga canciones de una popularidad en concreto? (y/n): '))
    if quierePopularidad == 'y':
        popularidad = int(input('Popularidad mínima(0-100): '))
    else:
        popularidad = None
    return popularidad
#endregion

#region PARAMETROS DE LA PLAYLIST

def parametroDuracion():
    quiereDuracion = str(input('Quieres que la playlist sea de una duración aproximada? (y/n): '))
    if quiereDuracion == 'y':
        duracion = int(input('Duración en minutos: '))
    else:
        duracion = None
    return duracion

def numero_canciones_min():
    quiereNumeroCancionesMin = str(input('Quieres que la playlist tenga un número mínimo de canciones? (y/n): '))
    if quiereNumeroCancionesMin == 'y':
        numero_canciones_min = int(input('Número mínimo de canciones: '))
    else:
        numero_canciones_min = None
    return numero_canciones_min

def coverPlaylist():
    quiereCover = str(input('Quieres que la playlist tenga una portada en concreto? (y/n): '))
    if quiereCover == 'y':
        cover = input('URL de la imagen: ')
    else:
        cover = None
    return cover

def parametrosUniversales(): #name, description, public
    playlist_name = str(input('Nombre de la playlist: '))
    playlist_description = str(input('Descripción de la playlist: '))
    playlist_public = str(input('Quieres que la playlist sea pública? (y/n): '))
    if playlist_public == 'y':
        playlist_public = True
    else:
        playlist_public = False
    return (playlist_name, playlist_description, playlist_public)
#endregion

#region COMPROBAR PARAMETROS (proceso de creación de la playlist)

def comprobar_artista(track, artistas): # artistas es una lista de artistas sacada del metodo parametroArtista
    for artista in artistas:
        if artista in track['track']['artists'][0]['id']: # si el artista está en la lista de artistas de la playlist
            return True
    return False

def comprobar_genero(track, generos, sp): # generos es una lista de generos sacada del metodo parametroGenero
    artista = track['track']['artists'][0]['id']
    info_artista = sp.artist(artista)
    for genre in info_artista['genres']:
        if genre in generos: # si el género está en la lista de géneros de la playlist
            return True
    return False

def comprobar_anio(track, anio_inicial, anio_final): # comprueba que el año del track esté entre los años inicial y final
    if anio_inicial <= int(track['track']['album']['release_date'].split('-')[0]) <= anio_final: # si el año de lanzamiento del album está entre los años inicial y final
        return True
    return False

def comprobar_album(track, albumes): # albumes es una lista de albumes sacada del metodo parametroAlbum
    for album in albumes:
        if album in track['track']['album']['id']:
            return True
    return False

def comprobar_duracion_min(track, duracion_canciones_min): # si la duracion minima es None, no se comprueba
    if duracion_canciones_min <= track['track']['duration_ms']/60000:
        return True
    return False

def comprobar_duracion_max(track, duracion_canciones_max): # si la duracion maxima es None, no se comprueba
    if track['track']['duration_ms']/60000 <= duracion_canciones_max:
        return True
    return False

def comprobar_popularidad(track, popularidad): # si la popularidad es None, no se comprueba
    if track['track']['popularity'] >= popularidad:
        return True
    return False
#endregion

#region UNA VEZ CREADA LA PLAYLIST

def comprobar_numero_canciones_min(playlist, numero_canciones_min): # si el numero de canciones minimas es None, no se comprueba
    if numero_canciones_min <= playlist['tracks']['total']:
        return True
    return False

def comprobar_cover(playlist, cover): # si el cover es None, no se comprueba
    if playlist['images'][0]['url'] == cover:
        return True
    return False

def comprobar_duracion(playlist, duracion): # duracion es la duracion aproximada de la playlist, del metodo parametroDuracion
    if duracion - 5 <= playlist['duration_ms']/60000 <= duracion + 5:
        return True
    return False

def comprobar_url_cover(cover):
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

#region CREAR PLAYLIST

def es_uri_valida(uri):
    # Utilizar una expresión regular para verificar el formato de la URI
    pattern = re.compile(r'^spotify:track:[a-zA-Z0-9]+$')
    return bool(pattern.match(uri))
def crear_playlist(dicParametros, sp, playlistOriginal):
    nombre_playlist = dicParametros['parametrosUniversales'][0]
    publica = dicParametros['parametrosUniversales'][2]
    descripcion_playlist = dicParametros['parametrosUniversales'][1]
    nueva_playlist = sp.user_playlist_create(user=sp.me()['id'], name=nombre_playlist, public=publica, description=descripcion_playlist)
    newTracks = []
    for item in playlistOriginal['items']:
        bool = False
        if dicParametros['artistas'] is not None:
            bool = comprobar_artista(item, dicParametros['artistas'])
        if dicParametros['generos'] is not None and bool:
            bool = comprobar_genero(item, dicParametros['generos'], sp)
        if dicParametros['años'] != (None, None) and bool:
            bool = comprobar_anio(item, dicParametros['años'][0], dicParametros['años'][1])
        if dicParametros['albumes'] is not None and bool:
            bool = comprobar_album(item, dicParametros['albumes'])
        if dicParametros['duracion_canciones_min'] is not None and bool:
            bool = comprobar_duracion_min(item, dicParametros['duracion_canciones_min'])
        if dicParametros['duracion_canciones_max'] is not None and bool:
            bool = comprobar_duracion_max(item, dicParametros['duracion_canciones_max'])
        if dicParametros['popularidad'] is not None and bool:
            bool = comprobar_popularidad(item, dicParametros['popularidad'])
        if bool:
            newTracks.append(item['track']['uri'])
    sp.playlist_add_items(nueva_playlist['id'], newTracks)
    return nueva_playlist
      
        
        
"""if dicParametros['cancionesMinimas'] != None: # si el numero de canciones minimas no es None, se comprueba que la playlist tenga ese numero de canciones minimas
    bool = comprobar_numero_canciones_min(nueva_playlist, dicParametros['cancionesMinimas'])
if dicParametros['duracionPlaylist'] != None and bool: # si la duracion de la playlist no es None, se comprueba que la playlist tenga esa duracion aproximada
    bool = comprobar_duracion(nueva_playlist, dicParametros['duracionPlaylist'])
if bool: # si la playlist cumple todos los parametros, se cambia la portada
    if dicParametros['cover'] != None and comprobar_url_cover(dicParametros['cover']):
        sp.playlist_upload_cover_image(nueva_playlist['id'], dicParametros['cover'])
    else:
        sp.playlist_upload_cover_image(nueva_playlist['id'], 'https://i.imgur.com/2r7bGfX.png')"""
#endregion