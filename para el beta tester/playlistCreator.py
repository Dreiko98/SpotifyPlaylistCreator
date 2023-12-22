import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistCreatorMetods import *
from flask import Flask, request, url_for, session, redirect
import time

#region Inicio de sesión

# initialize Flask app
app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

# set a random secret key to sign the cookie
app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

# route to handle logging in
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    print(auth_url)
    # redirect the user to the authorization URL
    return redirect(auth_url)

# route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('spotify_playlist_creator', _external=True))

# route to save the Discover Weekly songs to a playlist
@app.route('/spotifyPlaylistCreator')
def spotify_playlist_creator():
    try:
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print("User not logged in")
        return redirect('/')
    
    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    #region spotify_playlist_creator

    # recibir playlist original
    url_playlist = input('Ingresa la URL de la playlist original: ')
    id_playlist = get_id_playlist(url_playlist)
    playlistOriginal = sp.playlist_tracks(id_playlist, limit = 100) # playlist por paginas de 100 canciones
    playlist_info = sp.playlist(id_playlist)
    print(f'La playlist original es: {playlist_info["name"]}')

    # elegir parámetros para la playlist
    print('Cargando...')
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
    #endregion

    # CREAR PLAYLIST
    new_playlist = createPlaylist(parameters, sp, playlistOriginal)

# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', _external=False))

    # check if the token has expired, if it has, refresh it
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = 'cc2ece12ff0840e68932c542a3870c46',
        client_secret = '85fe48dc89d2469aa8a39ca57838e7e6',
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug=True)

#endregion