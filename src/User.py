import simplejson
import json
import urllib.request
import urllib.parse
import os

class User:

    oauth = None
    refresh_token = None

    USERS_URL = 'https://us-prof.np.community.playstation.net/userProfile/v1/users/'

    def __init__(self, tokens):
        self.oauth = tokens['oauth']
        self.refresh_token = tokens['refresh']

    def me(self):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        endpoint = 'me/profile2?fields=npId,onlineId,avatarUrls,plus,aboutMe,languagesUsed,trophySummary(@default,progress,earnedTrophies),isOfficiallyVerified,personalDetail(@default,profilePictureUrls),personalDetailSharing,personalDetailSharingRequestMessageFlag,primaryOnlineStatus,presences(@titleInfo,hasBroadcastData),friendRelation,requestMessageFlag,blocking,mutualFriendsCount,following,followerCount,friendsCount,followingUsersCount&avatarSizes=m,xl&profilePictureSizes=m,xl&languagesUsedLanguageSet=set3&psVitaTitleIcon=circled&titleIconSize=s'

        request = urllib.request.Request(self.USERS_URL+endpoint, headers=header)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))

        return data
