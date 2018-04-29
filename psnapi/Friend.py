import simplejson
import json
import requests
from psnapi.User import User

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

        response = requests.get(self.USERS_URL+endpoint, headers=header).text
        data = json.loads(response)

        friends = {}
        for i in data['profiles']:
            if i['presences'][0].get('titleName'):
                friends[i['onlineId']] = i['presences'][0]['titleName']
            else:
                friends[i['onlineId']] = ''
        return friends

    def send_friend_request(self, psn_id, request_message = ''):
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

        if request_message == '':
            request_message= 'Hola, soy '+onlineId+'. ¿Quieres ser mi amigo?'

        message = {
            "requestMessage": request_message
        }

        data = json.dumps(message)
        response = requests.post(self.USERS_URL+onlineId+'/friendList/'+psn_id, data=data, headers=header)

    def delete_friend_or_cancel_request(self, psn_id):
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

        response = requests.remove(self.USERS_URL+onlineId+'/friendList/'+psn_id, headers=header)

    def get_info(self, psn_id):
        endpoint = '/profile2?fields=npId,onlineId,avatarUrls,plus,aboutMe,languagesUsed,trophySummary(@default,progress,earnedTrophies),isOfficiallyVerified,personalDetail(@default,profilePictureUrls),personalDetailSharing,personalDetailSharingRequestMessageFlag,primaryOnlineStatus,presences(@titleInfo,hasBroadcastData),friendRelation,requestMessageFlag,blocking,mutualFriendsCount,following,followerCount,friendsCount,followingUsersCount&avatarSizes=m,xl&profilePictureSizes=m,xl&languagesUsedLanguageSet=set3&psVitaTitleIcon=circled&titleIconSize=s'
        url = self.USERS_URL+psn_id+endpoint

        header = {
            'Authorization': 'Bearer ' + self.oauth,
        }

        response = requests.get(url, headers=header).text

        return json.loads(response)

    def get_friends_of_friend(self, psn_id, limit = 36):
        endpoint = '/friends/profiles2?fields=onlineId,avatarUrls,plus,trophySummary(@default),isOfficiallyVerified,personalDetail(@default,profilePictureUrls),primaryOnlineStatus,presences(@titleInfo,hasBroadcastData)&sort=name-onlineId&avatarSizes=m&profilePictureSizes=m,xl&extendPersonalDetailTarget=true&offset=0&limit='+str(limit)
        url = self.USERS_URL+psn_id+endpoint

        header = {
            'Authorization': 'Bearer ' + self.oauth,
        }

        response = requests.get(url, headers=header).text

        return json.loads(response)
