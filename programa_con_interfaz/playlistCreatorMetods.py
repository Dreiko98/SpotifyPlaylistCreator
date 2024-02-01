import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import time
from PIL import Image # esta librería te permite abrir una imagen desde una url 
import spotify_ctk as sctk


def obtenerURLplaylist():
    url = ""
    input_dialog = sctk.Input_dialog(url)
    url = input_dialog.create_input_dialog()
    return url

def playlistLayer(root, playlistOriginal, playlist_info):
    trackList = []

    for item in playlistOriginal['items']:
        string = f"{item['track']['name']} - {item['track']['artists'][0]['name']}"
        trackList.append(string)

    title = playlist_info['name']
    cover = playlist_info['images'][0]['url']
    scrollable_tracks = sctk.scrollable_frame_playlist(trackList, 1550, 600, title, cover, root)
    scrollable_tracks.create_scrollable_frame()
    scrollable_tracks.add_cover()

    path = "assets\logo_solo.png"
    image_logo = sctk.image_label(1600, 50, path, (250, 250), root)
    image_logo.create_image_label()

    path = "assets\palabras-verdes.png"
    image_logo2 = sctk.image_label(642, 360, path, (636, 151.5), root)
    image_logo2.create_image_label()


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

#region ARTISTA
def printArtists(artistsList, sp): #imprimimos todos los artistas de la playlist con el formato: 1) nombre artista
    cont = 1
    for artist_ID in artistsList:
        info_artista = sp.artist(artist_ID)
        print(f'{cont}) {info_artista["name"]}')
        cont += 1

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



def artistParameter(playlistOriginal, playlist_info, sp, root, mi_variable_global):
    artistsDic = artistDicMaker(playlistOriginal, sp) # diccionario {nombreArtista:id}
    artists_name_list = list(artistsDic.keys()) # artistas de la playlist
    chosenArtists_names = []
    scrollable_artistas = sctk.scrollable_frame(artists_name_list, 30, 150, "disabled", "Artists", chosenArtists_names, root)
    scrollable_artistas.create_scrollable_frame()
    scrollable_artistas.create_submit_button(mi_variable_global)
    checkBox_artistas = sctk.general_checkBox(30, 112, "Quiero que mi playlist sea de un artista en concreto", scrollable_artistas, chosenArtists_names, root)
    checkBox_artistas.create_checkBox()


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

def albumParameter(playlistOriginal, playlist_info, sp, root, mi_variable_global):
    albumDic = albumDicMaker(playlistOriginal, sp)
    album_name_list = list(albumDic.keys()) # albumes de la playlist, lista de strings con los nombres de los albumes
    chosenAlbums_names = []
    scrollable_albums = sctk.scrollable_frame(album_name_list, 30, 600, "disabled", "Albums", chosenAlbums_names, root)
    scrollable_albums.create_scrollable_frame()
    scrollable_albums.create_submit_button(mi_variable_global)
    checkBox_albums = sctk.general_checkBox(30, 562, "Quiero que mi playlist sea de un album en concreto", scrollable_albums, chosenAlbums_names, root)
    checkBox_albums.create_checkBox()


def check_album(song, chosenAlbums, sp): # comprueba si el album de la canción está en la lista de albumes elegidos
    if chosenAlbums is not None:
        info_track = sp.track(song)
        if info_track['album']['id'] in chosenAlbums:
            return True
        return False
    return True
#endregion

#region AÑO

def yearRange(playlist, sp):
    yearList = []
    for item in playlist['items']:
        if item['track']['album']['id'] not in yearList:
            year = int(item['track']['album']['release_date'].split('-')[0])
            yearList.append(year)
    while playlist['next']:
        playlist = sp.next(playlist)
        for item in playlist['items']:
            if item['track']['album']['id'] not in yearList:
                year = int(item['track']['album']['release_date'].split('-')[0])
                yearList.append(year)
    return (min(yearList), max(yearList))

def yearParameter(root, playlistOriginal, sp):
    año_inicio = 0
    año_fin = 0
    año_min_playlist = yearRange(playlistOriginal, sp)[0]
    año_max_playlist = yearRange(playlistOriginal, sp)[1]
    list_years = []
    #x, y, min_año_playlist, max_año_playlist, año_inicio, año_fin, title1, title2, list_years, root
    year_slider = sctk.Slider(800, 142, año_min_playlist, año_max_playlist, año_inicio, año_fin, "Año de inicio", "Año de fin",list_years, root)
    year_slider.create_slider()
    year_slider.add_button()
    year_slider.create_disabling_checkBox()
    
    if list_years:
        return list_years
    list_years = None
    return list_years

def check_year(song, tuple_years, sp): # comprueba que el año del track esté entre los años inicial y final
    if tuple_years is not None:
        info_track = sp.track(song)
        songAlbum = info_track['album']
        if tuple_years[0] <= int(songAlbum['release_date'].split('-')[0]) <= tuple_years[1]: # si el año de lanzamiento del album está entre los años inicial y final
            return True
        return False
    return True

#endregion

# parametros de la playlist nueva

#region UNIVERSALES (nombre, descripcion, publica)

def universalParameters(root): #name, description, public

    playlist_name = []
    entry_nombre_playlist = sctk.entry(800, 738, "Nombre de la playlist...", playlist_name, root)
    entry_nombre_playlist.create_entry()
    entry_nombre_playlist.add_button()
    entry_nombre_playlist.add_label()


    playlist_description = []
    entry_descripcion_playlist = sctk.entry(800, 838, "Descripcion de la playlist...", playlist_description, root)
    entry_descripcion_playlist.create_entry()
    entry_descripcion_playlist.add_button()
    entry_descripcion_playlist.add_label()



    options = ["Playlist PRIVADA", "Playlist PUBLICA"]
    playlist_public = True
    segmented_button_privacidad = sctk.segmented_button(800, 938, playlist_public, options, root)
    segmented_button_privacidad.create_segmented_button()
    segmented_button_privacidad.add_label()

    return (playlist_name, playlist_public, playlist_description)
#endregion

#region COVER

def coverPlaylist(root):
    cover_url = []
    entry_cover = sctk.entry(800, 638, "URL de la imagen de la playlist...", cover_url, root)
    entry_cover.create_entry()
    entry_cover.add_button()
    entry_cover.add_label()

    if cover_url:
        return cover_url
    return None

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
    if check_year(song, dicParameters['years'], sp) == False:
        return False
    return True

def createPlaylist(sp, playlistOriginal, chosenArtists_names, chosenAlbums_names, years, playlist_name, playlist_description, playlist_public, cover_url, root):

    print(chosenAlbums_names) # None
    print(chosenArtists_names) # None

    if type(playlist_name) == list and len(playlist_name) == 0:
        playlist_name.append("no_name")
    if type(playlist_description) == list and len(playlist_description) == 0:
        playlist_description.append("no_description")
    if len(chosenAlbums_names) == 0:
        chosenAlbums_names = None
    else:
        chosenAlbums = []
        for album in chosenAlbums_names:
            chosenAlbums.append(albumDicMaker(playlistOriginal, sp)[album])
        chosenAlbums_names = chosenAlbums
    if len(chosenArtists_names) == 0:
        chosenArtists_names = None
    else:
        chosenArtists = []
        for artist in chosenArtists_names:
            chosenArtists.append(artistDicMaker(playlistOriginal, sp)[artist])
        chosenArtists_names = chosenArtists

    dicParameters = {}
    values = [chosenArtists_names, chosenAlbums_names, years, playlist_name[0], playlist_description[0], playlist_public, cover_url]
    print(values)
    keys = ['artists', 'albums', 'years', 'playlist_name', 'description', 'public', 'cover']
    for i in range(len(keys)):
        if values[i] != None:
            dicParameters[keys[i]] = values[i]
        else:
            dicParameters[keys[i]] = None

    # Suponiendo que 'token_info' contiene el token de acceso y la información relacionada
    user_id = sp.current_user()['id']  # Obtiene el ID del usuario autenticado con el token actual
    print(user_id)
    if user_id == sp.me()['id']: # si el usuario autenticado es el mismo que el usuario de la playlist original
        print('Ahora voy a intentar crear la playlist')
    try:
        print(sp.auth_manager.is_token_expired(sp.auth_manager.get_cached_token()))
        new_playlist = sp.user_playlist_create(user=user_id,
                                               name=dicParameters['playlist_name'],
                                               public=dicParameters['public'],
                                               description=dicParameters['description'])

    except spotipy.exceptions.SpotifyException as e:
        print(user_id)
        print("Ocurrió un error al intentar crear la playlist:")
        print(f"Mensaje de error: {e.msg}")
        print(f"Código de respuesta HTTP: {e.http_status}")
        print(f"Razón del error: {e.reason}")
        if e.http_status == 400:
            print("Esto usualmente indica que hay un problema con el JSON enviado.")
            # Imprime el JSON que intentaste enviar
            print("JSON que causó el error:", e.msg)
        return None

    original_tracklist = extraerCanciones(playlistOriginal, sp)
    new_tracklist = []
    print('Creando playlist...')
    for song in original_tracklist: #por cada id de cancion
        cumpleParams = cumpleParametros(song, dicParameters, sp)
        if cumpleParams:
            print(f'La canción {sp.track(song)["name"]} cumple los parámetros')
            new_tracklist.append(song)
            print(f'La canción {sp.track(song)["name"]} ha sido añadida a la playlist')
    while len(new_tracklist) > 100: # mientras grupos de 100 canciones por añadir
        añadirCanciones(new_tracklist[:100], new_playlist['id'], sp) # añadimos las 100 primeras canciones
        new_tracklist = new_tracklist[100:] # quitamos las 100 primeras canciones
        time.sleep(2) # esperamos 2 segundos para no sobrecargar la API
    añadirCanciones(new_tracklist, new_playlist['id'], sp) # añadimos las canciones restantes
    if dicParameters['cover'] is not None and check_url_cover(dicParameters['cover']):
        sp.playlist_upload_cover_image(new_playlist['id'], dicParameters['cover'])
    url_playlist = new_playlist['external_urls']['spotify']

    toplevelWindow = sctk.toplevel_window(root, url_playlist)
    toplevelWindow.create_toplevel_window()
#endregion