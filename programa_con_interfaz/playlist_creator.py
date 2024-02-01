import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistCreatorMetods import *
import os
from tkinter import *
import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
import spotify_ctk as sctk

def spotify_creator(sp):

    # Set the theme and color options
    ctk.set_appearance_mode("Dark") # Supported modes : Light, Dark, System
    ctk.set_default_color_theme("green") # Supported themes : green, dark-blue, blue

    root = ctk.CTk()
    root.title("Spotify Playlist Creator")  # Set title of the window
    root.geometry("1920x1080")
    root.iconbitmap("assets/icono.ico")


    # elegir parámetros para la playlist
    print('Cargando...')
    print('Ingresa los parámetros para la playlist nueva')


    url_playlist = obtenerURLplaylist()
    id_playlist = get_id_playlist(url_playlist)
    playlistOriginal = sp.playlist_tracks(id_playlist, limit = 100) # playlist por paginas de 100 canciones
    playlist_info = sp.playlist(id_playlist)
    print(f'La playlist original es: {playlist_info["name"]}')

    # playlist_layer
    playlistLayer(root, playlistOriginal, playlist_info)

    # ARTISTAS
    mi_variable_global = [[]]
    artistParameter(playlistOriginal, playlist_info, sp, root, mi_variable_global) # id de los artistas elegidos
    

    # ALBUM
    mi_variable_global2 = [[]]
    chosenAlbums = albumParameter(playlistOriginal, playlist_info, sp, root, mi_variable_global2) # id de los albums elegidos
    # parameters['albums'] = chosenAlbums

    # AÑO
    years = yearParameter(root, playlistOriginal, sp) # tupla con los años elegidos
    # parameters['years'] = years

    # COVER
    cover_url = coverPlaylist(root)
    # parameters['cover'] = cover_url
    #endregion

    #region universal parameters
    playlist_name, playlist_public, playlist_description = universalParameters(root)
    #endregion
    
    # DICPARAMETERS
    dicParameters = {}
    boton_final = ctk.CTkButton(root, text="Crear playlist", width=100, height=100, command = lambda: createPlaylist(sp, playlistOriginal, mi_variable_global[0], mi_variable_global2[0], years, playlist_name, playlist_description, playlist_public, cover_url, root))
    boton_final.place(x=1300, y=838)

    root.mainloop()


if __name__ == "__main__":

    REDIRECT_URI = 'http://localhost:5000/redirect'
    SCOPE = 'user-library-read playlist-modify-public playlist-modify-private'

    cache_file = '.cache' # o '.cache-username' con tu nombre de usuario de Spotify
    if os.path.exists(cache_file):
        os.remove(cache_file)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='CLIENT_ID',
                                                client_secret='CLIENT_SECRET
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE,
                                                cache_path=None,
                                                show_dialog=True)) # Forzar cuadro de diálogo

    spotify_creator(sp)