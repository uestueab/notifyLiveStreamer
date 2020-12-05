#!/usr/bin/env python3
#
# author:   Ablakim Giray Üstün
# date:     Sat 04 Jan 2020 07:38:00 PM CET
#
# descr:

import json
import requests
import notify2
import os
import urllib.request


class Streamer():

    def __init__(self):
        # The file that contains those streamers that you want to be notified of when they go online!
        self.favStreamerFile = '/tmp/streamer.txt'
        self.notifcationIcon = '/home/geeray/media/wallpapers/icons/cute.png'
        self.favoriteStreamers = [
                                    "epicenter_en1",
                                    "arteezy",
                                    "bububu",
                                    "eternalenvyy",
                                    "grandgrant",
                                    "masondota2",
                                    "matumbaman",
                                    "midone",
                                    "purgegamers",
                                    "singsing",
                                    "zai"
                                 ]

        self.headers = {
                        'Accept':        'application/vnd.twitchtv.v5+json',
                        'Client-ID':     '',
                        'Authorization': ''
                    }
        self.liveStreamers = []
        self.favStreamerLive = []

    def getLiveStreamers(self):
        response = requests.get('https://api.twitch.tv/kraken/streams/followed', headers=self.headers)
        data = json.loads(response.text)  # dictionary dump

        self.liveStreamers = list(map(lambda d: {
                                "display_name": d['channel']['display_name'],
                                "streamer":     d['channel']['name'],
                                "game":         d['channel']['game'],
                                "onlineSince":   d['created_at'],
                                "status":       d['channel']['status'],
                                }, data['streams']))


    def createFavStreamerFile(self):
        if not os.path.exists(self.favStreamerFile):
            os.mknod(self.favStreamerFile)

    # let programm be aware when streamer goes offline
    def updateStreamStatus(self):

        notify2.init('Twitch Streamer Notify')

        #favStreamerFile exists and has content..
        if os.path.getsize(self.favStreamerFile):
            # read/writable load favorite streams from file
            with open(self.favStreamerFile,'r+') as f:
                self.favStreamerLive = f.readlines()
                self.favStreamerLive = [fav for fav in self.favStreamerLive]

                # put values from each streamer dictionary to a list
                # so that we can iterate over them
                liveStreamersList = list(map(lambda s: s.get('streamer'), self.liveStreamers))

                # flush the file
                f.seek(0)
                f.truncate()




                # print([x.split(' ')[0] for x in self.favStreamerLive])
                # write the streamer to file again only if they're still among the live streamers
                for fav in self.favStreamerLive:
                    if fav.split(" ")[0] in liveStreamersList:
                        f.write(fav)
                    else:
                        n = notify2.Notification("{} is offline!".format(s),
                                 "see you soon..".format(s),
                                 self.notifcationIcon
                                 )
                        n.show()
                f.close()

    def notifyOnlineStreamer(self):

        notify2.init('Twitch Streamer Notify')
        streamInfo = ""

        for s in self.liveStreamers:
            if s["streamer"] in self.favoriteStreamers:
                with open(self.favStreamerFile,'r+') as f:
                    self.favStreamerLive = f.readlines()
                    self.favStreamerLive = [streamer for streamer in self.favStreamerLive] # error on


                    if s["streamer"] not in [f.split(" ",1)[0] for f in self.favStreamerLive]: # streamer was not found in file -> streamer is new
                        n = notify2.Notification("{} is online!".format(s['display_name']),
                                    "Playing: {}\n{}".format(s['game'],s['status']),
                                    self.notifcationIcon
                                    )
                        n.show()

                        for key, value in s.items():
                            if key == "display_name":
                                continue

                            elif key == "game":
                                value = "".join(value.split())


                            streamInfo += value +  " "

                        f.write(streamInfo + '\n')
                        streamInfo = ""


                    f.close()


# The main function
if __name__== "__main__":


    streamer = Streamer()
    streamer.createFavStreamerFile()
    streamer.getLiveStreamers()
    # uncomment lines below for debugging
    # streamer.liveStreamers.append({'streamer': 'purgegamers', 'display_name': 'purgeTV'}) # fake online
    # streamer.liveStreamers.pop() # fake offline
    # print(streamer.liveStreamers)
    streamer.updateStreamStatus()
    streamer.notifyOnlineStreamer()

