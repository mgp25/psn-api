import simplejson
import json
import urllib.request
import urllib.parse
import os
from psn_api.User import User

class Friend:

    oauth = None
    refresh_token = None

    USERS_URL = 'https://us-prof.np.community.playstation.net/userProfile/v1/users/'

    def __init__(self, tokens):
        self.oauth = tokens['oauth']
        self.refresh_token = tokens['refresh']

    def my_friends(self, filter = 'online', limit = 36):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        endpoint = 'me/friends/profiles2?fields=onlineId,avatarUrls,following,friendRelation,isOfficiallyVerified,personalDetail(@default,profilePictureUrls),personalDetailSharing,plus,presences(@titleInfo,hasBroadcastData,lastOnlineDate),primaryOnlineStatus,trophySummary(@default)&sort=name-onlineId&userFilter='+filter+'&avatarSizes=m&profilePictureSizes=m&offset=0&limit='+str(limit)

        request = urllib.request.Request(self.USERS_URL+endpoint, headers=header)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))

        friends = {}
        for i in data['profiles']:
            if i['presences'][0].get('titleName'):
                friends[i['onlineId']] = i['presences'][0]['titleName']
            else:
                friends[i['onlineId']] = ''
        return friends

    def add(self, psn_id, request_message = ''):
        tokens = {
            'oauth': self.oauth,
            'refresh': self.refresh_token
        }
        user = User(tokens)
        onlineId = user.me()['profile']['onlineId']

        header = {
            'Authorization': 'Bearer ' + self.oauth,
            'Content-Type': 'application/json; charset=utf-8'
        }

        message = {
            "requestMessage": request_message
        }
        data = urllib.parse.urlencode(message).encode('utf-8')
        request = urllib.request.Request(self.USERS_URL+onlineId+'/friendList/'+psn_id, headers=header, data=data)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        return data
