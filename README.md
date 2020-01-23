# notifyLiveStreamer



Specify some Twitch streamers and get notified when they go online.
(Tested on Linux)

### Other features:
  - get notified when streamer of choice goes offline

### Installation

Before running the code, make sure that you installed all required modules and have a valid client-id as well as a oauth. Finally edit these lines below in notifyLiveStreamer.py

```python
self.favStreamerFile = '/path/of/file'
self.notifcationIcon = '/path/of/icon' #add an icon to your notifications
self.favoriteStreamers = ["streamer1","streamer2","streamer3"]
self.headers = {
                'Accept':        'application/vnd.twitchtv.v5+
                'Client-ID':     'your client_id',
                'Authorization': 'your oauth'
            }

```


### Modules

The following modules were used. You may have to install them on your system first.

| Module |  |
| ------ | ------ |
| notify2 |communicate with the notification server |
| requests ||


License
----

MIT

