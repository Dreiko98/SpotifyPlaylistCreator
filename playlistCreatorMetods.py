#buscador de album por nombre
#que salgan solo los albumes de los artistas que has seleccionado

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import re
from difflib import get_close_matches
import sys
import time

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

# parametros de las canciones

def buscador_nombres(nombre_a_buscar, lista_nombres, n = 5, umbral = 0.3):
    nombres_busqueda = get_close_matches(nombre_a_buscar, lista_nombres, n, umbral)
    return nombres_busqueda if nombres_busqueda else None


#region ARTISTA

def artistDicMaker(playlist, sp): #diccionario {nombreArtista:id}
    artistDic = {}
    for item in playlist['items']: # iteramos sobre cada canción de la playlist
        for artist in item['track']['artists']:# iteramos sobre cada artista de la canción
            if artist['id'] not in artistDic.values():
                artistDic[artist['name']] = artist['id']
    while playlist['next']: # mientras haya páginas adicionales
        playlist = sp.next(playlist) # solicitud para obtener la página siguiente
        for item in playlist['items']: # iteramos sobre cada canción de la playlist
            for artist in item['track']['artists']:# iteramos sobre cada artista de la canción
                if artist['id'] not in artistDic.values():
                    artistDic[artist['name']] = artist['id']
    return artistDic


def printArtists(artistsList, sp): #imprimimos todos los artistas de la playlist con el formato: 1) nombre artista
    cont = 1
    for artist_ID in artistsList:
        info_artista = sp.artist(artist_ID)
        print(f'{cont}) {info_artista["name"]}')
        cont += 1

def chooseArtists(artistsDic, sp): # devuelve chosenArtists, una lista
    chosenArtists = []
    while True:
        nombre_a_buscar = str(input("Introduce el nombre del artista:"))
        artists_prox = buscador_nombres(nombre_a_buscar, list(artistsDic.keys())) # si no lo encuentra, devuelve None, si lo encuentra, devuelve una lista con los nombres   
        atists_prox_id = []
        for artist in artists_prox:
            atists_prox_id.append(artistsDic[artist]) # lista de ids de los artistas que ha encontrado
        if artists_prox:
            printArtists(atists_prox_id, sp)
            chosenArtistNum = int(input("Introduce el número del artista que buscas:"))
            chosenArtistName = artists_prox[chosenArtistNum-1] # nombre del artista que ha elegido
            print(chosenArtistName)
            chosenArtistID = artistsDic.get(chosenArtistName, None)
            if chosenArtistID is None:
                print(f"No se encontró {chosenArtistName}, de tipo {type(chosenArtistName)} en el diccionario.")
            chosenArtists.append(chosenArtistID)
        else: print('Artista no encontrado')
        buscarOtro = str(input("¿Quieres buscar otro artista?(y,n): "))
        if buscarOtro.lower() == "n":
            break
    return chosenArtists

def artistParameter(playlistOriginal, playlist_info, sp):
    artistsDic = artistDicMaker(playlistOriginal, sp) # artistas de la playlist
    wantsArtist = str(input('¿Quieres que la playlist sea de un artista en concreto? (y/n): '))  
    if wantsArtist.lower() == 'y':
        chosen_artists = chooseArtists(artistsDic, sp)
        return chosen_artists if chosen_artists else None
    return None


def check_artist(song, chosenArtists, sp): # comprueba si almenos algún artista de la canción está en la lista de artistas elegidos
    if chosenArtists is not None:
        info_track = sp.track(song)
        for artist in info_track['artists']:
            if artist['id'] in chosenArtists:
                return True
        return False
    return True

#endregion

#region ALBUM

def albumDicMaker(playlist, sp):
    albumDic = {}
    for item in playlist['items']:
        if item['track']['album']['id'] not in albumDic.values() and item['track']['album']['album_type'] == 'album':
            album_name = item['track']['album']['name']
            album_id = item['track']['album']['id']
            albumDic[album_name] = album_id
    while playlist['next']:
        playlist = sp.next(playlist)
        for item in playlist['items']:
            if item['track']['album']['id'] not in albumDic.values() and item['track']['album']['album_type'] == 'album':
                album_name = item['track']['album']['name']
                album_id = item['track']['album']['id']
                albumDic[album_name] = album_id
    return albumDic

def printAlbums(albumList, sp): # imprime todos los albumes de la playlist con el formato: 1) nombre album
    cont = 1
    for album_ID in albumList:
        info_album = sp.album(album_ID)
        print(f'{cont}) {info_album["name"]}')
        cont += 1

def chooseAlbum(albumDic, sp):
    chosenAlbums = []
    while True:
        nombre_a_buscar = str(input("Introduce el nombre del álbum:"))
        albums_prox = buscador_nombres(nombre_a_buscar, list(albumDic.keys())) # si no lo encuentra, devuelve None, si lo encuentra, devuelve una lista con los nombres   
        albums_prox_id = []
        for album in albums_prox:
            albums_prox_id.append(albumDic[album])
        if type(albums_prox) == list:
            printAlbums(albums_prox_id, sp)
            chosenAlbumNum = int(input("Introduce el número del álbum que buscas:"))
            chosenAlbumName = albums_prox[chosenAlbumNum-1] # nombre del album que ha elegido
            print(chosenAlbumName)
            chosenAlbumID = albumDic.get(chosenAlbumName, None)
            if chosenAlbumID is None:
                print(f"No se encontró {chosenAlbumName}, de tipo {type(chosenAlbumName)} en el diccionario.")
            chosenAlbums.append(chosenAlbumID)
        elif type(albums_prox) == str:
            chosenAlbums.append(albums_prox)
        else: print('Álbum no encontrado')
        buscarOtro = str(input("¿Quieres buscar otro álbum?(y,n): "))
        if buscarOtro.lower() == "n":
            break
    return chosenAlbums

def albumParameter(playlistOriginal, playlist_info, sp):
    albumDic = albumDicMaker(playlistOriginal, sp)
    wantsAlbum = str(input('¿Quieres que la playlist sea de un álbum en concreto? (y/n): '))
    if wantsAlbum.lower() == 'y':
        chosen_albums = chooseAlbum(albumDic, sp)
        return chosen_albums if chosen_albums else None
    return None

def check_album(song, chosenAlbums, sp): # comprueba si el album de la canción está en la lista de albumes elegidos
    if chosenAlbums is not None:
        info_track = sp.track(song)
        if info_track['album']['id'] in chosenAlbums:
            return True
        return False
    return True
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

def check_year(song, initial_year, end_year, sp): # comprueba que el año del track esté entre los años inicial y final
    if initial_year is not None and end_year is not None:
        info_track = sp.track(song)
        songAlbum = info_track['album']
        if initial_year <= int(songAlbum['release_date'].split('-')[0]) <= end_year: # si el año de lanzamiento del album está entre los años inicial y final
            return True
        return False
    return True

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

def check_popularity(song, popularity, sp): # si la popularidad es None, no se comprueba
    if popularity is not None:
        info_track = sp.track(song)
        if info_track['popularity'] >= popularity:
            return True
        return False
    return True

#endregion

# parametros de la playlist nueva

#region UNIVERSALES (nombre, descripcion, publica)

def universalParameters(): #name, description, public
    playlist_name = str(input('Nombre de la playlist: '))
    playlist_description = str(input('Descripción de la playlist: '))
    playlist_public = str(input('Quieres que la playlist sea pública? (y/n): '))
    if playlist_public == 'y':
        playlist_public = True
    else:
        playlist_public = False
    return (playlist_name, playlist_public, playlist_description)

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

# crear playlist

#region CREAR PLAYLIST

def extraerCanciones(playlist, sp): #devuelve en una lista los ids de las canciones de una playlist que recibe como parámetro
    trackList = []
    for item in playlist['items']:
        trackList.append(item['track']['id'])
    while playlist['next']:
        playlist = sp.next(playlist)
        for item in playlist['items']:
            trackList.append(item['track']['id'])
    return trackList

def añadirCanciones(listaTracks, nuevaPlaylistID, sp): #añade a una playlist una lista de canciones
    sp.playlist_add_items(nuevaPlaylistID, listaTracks) 
    print('Canciones añadidas a la playlist, ve a disfrutar de tu nueva música!')

"""# Verifica si hay más páginas y realiza solicitudes adicionales si es necesario
while results['next']: # Mientras haya páginas adicionales
    results = sp.next(results) # Solicitud para obtener la página siguiente
    for item in results['items']:
        # Realiza la operación que necesites con cada elemento de las páginas adicionales
        print(item['track']['name'])"""


def cumpleParametros(song, dicParameters, sp): # song es el id de la canción
    if check_artist(song, dicParameters['artists'], sp) == False:
        return False
    if check_album(song, dicParameters['albums'], sp) == False:
        return False
    if check_year(song, dicParameters['years'][0], dicParameters['years'][1], sp) == False:
        return False
    if check_popularity(song, dicParameters['popularity'], sp) == False:
        return False
    return True

def createPlaylist(dicParameters, sp, playlistOriginal):
    playlist_name, playlist_public, playlist_description = universalParameters()
    new_playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public = playlist_public, description=playlist_description)
    new_tracklist = []
    print('Creando playlist...')
    for song in extraerCanciones(playlistOriginal, sp): #por cada id de cancion
        cumpleParams = cumpleParametros(song, dicParameters, sp)
        if cumpleParams:
            new_tracklist.append(song)
    añadirCanciones(new_tracklist, new_playlist['id'], sp)
    if dicParameters['cover'] is not None and check_url_cover(dicParameters['cover']):
        sp.playlist_upload_cover_image(new_playlist['id'], dicParameters['cover'])
    new_url = new_playlist['external_urls']['spotify'] # devuelve la url de la playlist creada
    print(f'La playlist {playlist_name} ha sido creada con éxito. Puedes acceder a ella en {new_url}')
#endregion