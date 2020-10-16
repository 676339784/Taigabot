from util import formatting, hook, http, web
import re

from util import hook, http, web
from urllib import urlencode
import requests

gateway = 'http://open.spotify.com/{}/{}'  # http spotify gw address
spuri = 'spotify:{}:{}'
@@ -11,96 +10,230 @@
           '([a-zA-Z0-9]+))', re.I)


def sptfy(inp, sptfy=False):
    if sptfy:
        shortenurl = "http://sptfy.com/index.php"
        data = urlencode({'longUrl': inp, 'shortUrlDomain': 1, 'submitted': 1, "shortUrlFolder": 6, "customUrl": "",
                          "shortUrlPassword": "", "shortUrlExpiryDate": "", "shortUrlUses": 0, "shortUrlType": 0})
        try:
            soup = http.get_soup(shortenurl, post_data=data, cookies=True)
        except:
            return inp
        try:
            link = soup.find('div', {'class': 'resultLink'}).text.strip()
            return link
        except:
            message = "Unable to shorten URL: %s" % \
                      soup.find('div', {'class': 'messagebox_text'}).find('p').text.split("<br/>")[0]
            return message
    else:
        return web.try_isgd(inp)
def get_access_token(client_id, client_secret):
    """ Get Spotify access token based on client_id and client_secret
    Required to use Spotify's search APIs
    """

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token


@hook.command('sp')
@hook.command
def spotify(inp):
def spotify(inp, bot=None):
    """spotify <song> -- Search Spotify for <song>"""

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Query track
    try:
        data = http.get_json("http://ws.spotify.com/search/1/track.json", q=inp.strip())
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': inp, 'type': 'track'}
        data = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)
        data = data.json()
    except Exception as e:
        return "Could not get track information: {}".format(e)

    # Parsing data and returning
    try:
        type, id = data["tracks"][0]["href"].split(":")[1:]
        first_result = data["tracks"]["items"][0]
        artists = []
        for a in first_result["artists"]:
            artists.append(a["name"])
        artist = ', '.join(artists)
        track = first_result["name"]
        album = first_result["album"]["name"]
        url = first_result["external_urls"]["spotify"]
        uri = first_result["uri"]
        song_query_output = "\"{}\" by \x02{}\x02 from the album \x02{}\x02 - {} ({})".format(
            track, artist, album, url, uri)
    except IndexError:
        return "Could not find track."
    url = sptfy(gateway.format(type, id))
    return u"\x02{}\x02 by \x02{}\x02 - \x02{}\x02".format(data["tracks"][0]["name"],
                                                           data["tracks"][0]["artists"][0]["name"], url)

    return formatting.output('Spotify', [song_query_output])


@hook.command('album')
@hook.command
def spalbum(inp):
def spalbum(inp, bot=None):
    """spalbum <album> -- Search Spotify for <album>"""

    # Get access token
    try:
        data = http.get_json("http://ws.spotify.com/search/1/album.json", q=inp.strip())
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Query artist
    try:
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': inp, 'type': 'album'}
        data = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)
        data = data.json()

    except Exception as e:
        return "Could not get album information: {}".format(e)

    # Parsing data and returning
    try:
        type, id = data["albums"][0]["href"].split(":")[1:]
        first_result = data["albums"]["items"][0]
        artists = []
        for a in first_result["artists"]:
            artists.append(a["name"])
        artist = ', '.join(artists)
        album = first_result["name"]
        url = first_result["external_urls"]["spotify"]
        uri = first_result["uri"]
        album_query_output = "\x02{}\x02 - \x02{}\x02 - {} ({})".format(
            artist, album, url, uri)
    except IndexError:
        return "Could not find album."
    url = sptfy(gateway.format(type, id))
    return u"\x02{}\x02 by \x02{}\x02 - \x02{}\x02".format(data["albums"][0]["name"],
                                                           data["albums"][0]["artists"][0]["name"], url)

    return formatting.output('Spotify', [album_query_output])


@hook.command('artist')
@hook.command
def spartist(inp):
def spartist(inp, bot=None):
    """spartist <artist> -- Search Spotify for <artist>"""

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Query artist
    try:
        data = http.get_json("http://ws.spotify.com/search/1/artist.json", q=inp.strip())
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': inp, 'type': 'artist'}
        data = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)
        data = data.json()
        print(data)
    except Exception as e:
        return "Could not get artist information: {}".format(e)

    # Parsing data and returning
    try:
        type, id = data["artists"][0]["href"].split(":")[1:]
        first_result = data["artists"]["items"][0]
        artist = first_result["name"]
        genres = ', '.join(first_result["genres"])
        url = first_result["external_urls"]["spotify"]
        uri = first_result["uri"]
        artist_query_output = "\x02{}\x02, Genres: {} - {} ({})".format(
            artist, genres, url, uri)
    except IndexError:
        return "Could not find artist."
    url = sptfy(gateway.format(type, id))
    return u"\x02{}\x02 - \x02{}\x02".format(data["artists"][0]["name"], url)

    return formatting.output('Spotify', [artist_query_output])


@hook.regex(*http_re)
@hook.regex(*spotify_re)
def spotify_url(match):
def spotify_url(match, bot=None):
    """ Match spotify urls and provide blurb and track
    """

    # Regex match on spotify urls and see if url links to track/album/artist
    type = match.group(2)
    spotify_id = match.group(3)
    url = spuri.format(type, spotify_id)
    # no error catching here, if the API is down fail silently
    data = http.get_json("http://ws.spotify.com/lookup/1/.json", uri=url)

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Set appropriate headers
    headers = {'Authorization': 'Bearer ' + access_token}

    # Parse track link and retrieve data for blurb
    if type == "track":
        name = data["track"]["name"]
        artist = data["track"]["artists"][0]["name"]
        album = data["track"]["album"]["name"]
        return u"Spotify Track: \x02{}\x02 by \x02{}\x02 from the album \x02{}\x02 - \x02{}\x02".format(name, artist,
                                                                                                        album, sptfy(
                gateway.format(type, spotify_id)))
    elif type == "artist":
        return u"Spotify Artist: \x02{}\x02 - \x02{}\x02".format(data["artist"]["name"],
                                                                 sptfy(gateway.format(type, spotify_id)))
    elif type == "album":
        return u"Spotify Album: \x02{}\x02 - \x02{}\x02 - \x02{}\x02".format(data["album"]["artist"],
                                                                             data["album"]["name"],
                                                                             sptfy(gateway.format(type, spotify_id)))
        try:
            data = requests.get('https://api.spotify.com/v1/tracks/{}'.format(spotify_id),
                                headers=headers)
            data = data.json()
        except Exception as e:
            return "Could not get album information: {}".format(e)

        try:
            first_result = data
            artists = []
            for a in first_result["artists"]:
                artists.append(a["name"])
            artist = ', '.join(artists)
            track = first_result["name"]
            album = first_result["album"]["name"]
            song_query_output = "\"{}\" by \x02{}\x02 from the album \x02{}\x02".format(
                track, artist, album)
        except IndexError:
            return "Could not find track."

        return formatting.output('Spotify', [song_query_output])

    # Parse album link and retrieve data for blurb
    if type == "album":
        try:
            data = requests.get('https://api.spotify.com/v1/albums/{}'.format(spotify_id),
                                headers=headers)
            data = data.json()
        except Exception as e:
            return "Could not get album information: {}".format(e)

        try:
            first_result = data
            artists = []
            for a in first_result["artists"]:
                artists.append(a["name"])
            artist = ', '.join(artists)
            album = first_result["name"]
            album_query_output = "\x02{}\x02 - \x02{}\x02".format(
                artist, album)
        except IndexError:
            return "Could not find album."

        return formatting.output('Spotify', [album_query_output])

    # Parse artist link and retrieve data for blurb
    if type == "artist":
        try:
            data = requests.get('https://api.spotify.com/v1/artists/{}'.format(spotify_id),
                                headers=headers)
            data = data.json()
        except Exception as e:
            return "Could not get artist information: {}".format(e)

        try:
            first_result = data
            artist = first_result["name"]
            genres = ', '.join(first_result["genres"])
            artist_query_output = "\x02{}\x02, Genres: {}".format(
                artist, genres)
        except IndexError:
            return "Could not find artist."

        return formatting.output('Spotify', [artist_query_output])
