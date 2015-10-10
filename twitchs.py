
import urllib
import json
import os
import easygui as eg
import urllib2

def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    url = 'https://api.twitch.tv/kraken/streams/' + user
    try:
        info = json.loads(urllib2.urlopen(url, timeout=15).read().decode('utf-8'))
        if info['stream'] == None:
            status = 1
        else:
            status = 0
    except urllib2.URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    return status
def loadStream(user,quality):
    if check_user(user) == 0:
        os.system("livestreamer twitch.tv/" + user +' '+ quality)
    elif check_user(user) == 1:
        eg.msgbox(msg='User Offline: ', title='Offline')
        main()
    else:
        eg.msgbox(msg="channel not found", title='not found')
        main()
def game_channels(game):
    streams = 0
    url = 'https://api.twitch.tv/kraken/streams/?game='+game
    try:
        info = urllib.urlopen(url)
        streamers_data = json.loads(info.readlines()[0])
        streams = [stream['channel']['display_name'] for stream in streamers_data['streams']]

    except urllib2.URLError as e:
        print 'error'
    if streams:
        return streams
    else:
        main()
def list_streams_ui(streams,game):
    msg = "choose your "+game+" stream"
    title = 'Choose stream'
    choices = streams
    choicebox = eg.choicebox(msg,title,choices)
    if choicebox:
        return choicebox
    else:
        main()
def game_chosing():
    choices = ["Dota 2","League of Legends","Hearthstone: Heroes of warcraft","path of exile","Heroes of the storm",'other']
    game = eg.choicebox(msg='choose game',title="Choose game, press cancel to exit",choices = choices)
    if game :
        if game == 'other':
            game = eg.enterbox(msg = 'enter the game',title='enter other game')
            return game
        else:
            return game
    else:
        exit()
def get_quality():
    q = ['mobile','low','medium','high','source']
    quality = eg.choicebox(msg='Choose video quality(mobile worst, source best)',title='Video quality',choices = q)
    if quality:
        return quality
    else:
        main()
def main():
    game = game_chosing()
    loadStream(list_streams_ui(game_channels(game),game),get_quality())
main()

