# OBS Windows Now Playing

This script gather the now playing title from the Windows api.
Therefore, it's compatible with any media player that publish the track information trough this api.

Reported working with:
* Deezer (app)
* Spotify (app/web chromium/web firefox)
* YouTube (web chromium / web firefox)
* Also, probably other websites that enable playback control via the multimedia keys 

It updates the current title into a custom data in wize bot streaming tool.

It also can update a local text field to display on stream / debug

## Setup

1. Install [Python for Windows](https://www.python.org/downloads/windows/) (tested with 3.11)
2. Install winsdk package
   
    From a command prompt or powershell run the following command in the python install directory:
    ```.\python.exe -m pip install winsdk==1.0.0b9```
3. Log onto your Wize Bot account and gather the apikey:
   
    ![wizebot-apikey](https://github.com/thelan/obs-windows-nowplaying/blob/master/doc/wizebot-apikey.png?raw=true)

   If you don't want to use an online service you can also add a text source to update 
4. Open OBS and go to scripts
   
   ![OBS-add-script](https://github.com/thelan/obs-windows-nowplaying/blob/master/doc/step-add-script.png?raw=true)

   Tell OBS where you have installed python

   ![configure-python](https://github.com/thelan/obs-windows-nowplaying/blob/master/doc/configure-python.png?raw=true)

    Add the script `wizebot-now-playing.py` from the src directory to OBS and configure it

   ![OBS-Configure-script](https://github.com/thelan/obs-windows-nowplaying/blob/master/doc/step-config-script.png?raw=true)
5. Configure Wize Bot to use the Custom data
    
   Eg: use the tag in a command response using  `$custom_data(obs-np)`. Replace `obs-np` to match the key you put in the settings

## More info

For more information please read Wize Bot documentation about custom datas:
https://support.wizebot.tv/docs/api_custom_datas
