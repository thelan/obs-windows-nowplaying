import obspython as obs
import asyncio

import urllib.error
import urllib.parse
import urllib.request

from winsdk.windows.media import MediaPlaybackType
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager


# -----
# User overridable variables
apikey = ""
wizebot_field = "obs-np"
interval = 10
source_name = ""
# -----

# -----
# Internal variables
last_data = None
# ------------------------------------------------------------


## See https://stackoverflow.com/a/66037406
async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

    return


def set_wizebot_custom_data(api_key, key, value):
    url = 'https://wapi.wizebot.tv/api/custom-data/{}/set/{}/{}'.format(api_key, key, urllib.parse.quote(value))
    try:
        req = urllib.request.Request(url, method='POST')
        urllib.request.urlopen(req)
        obs.script_log(obs.LOG_INFO, "Wise bot updated")

    except urllib.error.URLError as err:
        obs.script_log(obs.LOG_WARNING, "Error opening URL '" + url + "': " + err.reason)
        obs.remove_current_callback()


def update_text():
    global apikey, wizebot_field, interval, source_name, last_data
    try:
        media_info = asyncio.run(get_media_info())

        # Filter non music media
        if media_info['playback_type'] != MediaPlaybackType.MUSIC:
            return

    except OSError:
        obs.script_log(obs.LOG_WARNING, "Failed to get now playing")
        return
    now_playing = '{} - {}'.format(media_info['title'], media_info['artist'])

    # Skip update if nothing changed
    if last_data == now_playing:
        return

    last_data = now_playing

    obs.script_log(obs.LOG_INFO, "Now playing '" + now_playing + "'")
    if apikey != '' and wizebot_field != '':
        set_wizebot_custom_data(apikey, wizebot_field, now_playing)

    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", '{}         '.format(now_playing))
        obs.obs_source_update(source, settings)
        obs.obs_source_release(source)


def refresh_pressed(props, prop):
    update_text()


def script_description():
    return "Update a now playing variable on Wize bot detecting the song using Windows API.\n\nBy thelan"


def script_update(settings):
    global apikey, wizebot_field, interval, source_name

    apikey = obs.obs_data_get_string(settings, "apikey")
    wizebot_field = obs.obs_data_get_string(settings, "wizebot_field")
    interval = obs.obs_data_get_int(settings, "interval")
    source_name = obs.obs_data_get_string(settings, "source")

    obs.timer_remove(update_text)

    obs.timer_add(update_text, interval * 1000)


def script_defaults(settings):
    global interval, wizebot_field
    obs.obs_data_set_default_int(settings, "interval", interval)
    obs.obs_data_set_default_string(settings, "wizebot_field", wizebot_field)


def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "apikey", "Wize Bot API Token", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "wizebot_field", "Wize Bot Custom Data", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "interval", "Update Interval (seconds)", 5, 60, 1)

    p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)

        obs.source_list_release(sources)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props
