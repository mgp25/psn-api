import simplejson
import json
import requests
import random
from hyper import HTTP20Connection
import logging
import os.path
from psnapi.User import User

class Messaging:

    oauth = None
    refresh_token = None
    me = None

    MESSAGE_THREADS_URL = 'https://es-gmsg.np.community.playstation.net/groupMessaging/v1/threads'
    MESSAGE_USERS_URL = 'https://es-gmsg.np.community.playstation.net/groupMessaging/v1/users/'
    SEND_MESSAGE_URL = 'https://es-gmsg.np.community.playstation.net/groupMessaging/v1/messageGroups/'

    def __init__(self, tokens):
        self.oauth = tokens['oauth']
        self.refresh_token = tokens['refresh']

        tokens = {
            'oauth': self.oauth,
            'refresh': self.refresh_token
        }

        user = User(tokens)
        self.me = user.me()['profile']['onlineId']

    def get_all_groups(self):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        url = self.MESSAGE_THREADS_URL + "/?fields=threadMembers,threadNameDetail,threadThumbnailDetail,threadProperty,latestMessageEventDetail,latestTakedownEventDetail,newArrivalEventDetail&limit=200&offset=0"
        response = requests.get(url, headers=header).text
        data = json.loads(response)

        return data

    def get_favorite_groups(self):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        url = self.MESSAGE_THREADS_URL + "/?fields=threadMembers,threadNameDetail,threadThumbnailDetail,threadProperty,latestMessageEventDetail,latestTakedownEventDetail,newArrivalEventDetail&limit=200&offset=0&filter=favorite"
        response = requests.get(url, headers=header).text
        data = json.loads(response)

        return data

    def remove_group(self, group_id):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        url = self.MESSAGE_THREADS_URL + "/" + group_id + "/users/me"
        response = requests.remove(url, headers=header)

    def favorite_group(self, group_id):
        self.set_favorite_group(group_id, True)

    def unfavorite_group(self, group_id):
        self.set_favorite_group(group_id, False);

    def set_favorite_group(self, group_id, flag):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.oauth
        }

        url = self.MESSAGE_USERS_URL  + "me/threads/" + group_id + "/favorites"

        payload = {"favoriteDetail": {"favoriteFlag": flag}}
        payload = json.dumps(payload)

        response = requests.put(url, headers=header, data=payload)

    def send_message(self, thread_id, message_text = "", attachment = "", message_type = 1, audio_length = ""):

        boundary = "---------------------------"+str(random.sample(range(10000, 99999), 1)[0])
        header = {
            'origin': 'https://my.playstation.com',
            'Authorization': 'Bearer ' + self.oauth,
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Content-Type': 'multipart/mixed; boundary='+boundary,
            'accept-encoding': 'gzip, deflate, br',
            'accept': '*/*',
            'dnt': '1',

        }

        headers_auth = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'accept-encoding': 'gzip, deflate, br',
            'access-control-request-method': 'POST',
            'access-control-request-headers': 'authorization,content-type',
            'origin': 'https://my.playstation.com',
            'dnt': '1'
        }

        message_body = {
            "message": {
                "messageKind": 1,
                "body": message_text
            }
        }

        message = "\r\n"
        message += boundary+"\r\n"
        message += "Content-Type: application/json; charset=utf-8\r\n"
        message += "Content-Description: message\r\n"
        message += "\r\n"
        message += json.dumps(message_body) + "\r\n"
        message += boundary + "--\r\n"


        conn = HTTP20Connection("es-gmsg.np.community.playstation.net:443")
        auth = conn.request('OPTIONS', "/groupMessaging/v1/messageGroups/"+thread_id+"/messages", headers=headers_auth)
        auth_response = conn.get_response(auth)
        request = conn.request('POST', "/groupMessaging/v1/messageGroups/"+thread_id+"/messages", headers=header, body=message)
        response = conn.get_response(request)
        print(response.read())

        return response


        '''
        users_body = {
            "threadDetail": {
                "threadMembers": {}
            }
        }

        if (isinstance(psn_ids, list)):
            i = 0
            for psn_id in psn_ids:
                users_body["threadDetail"]["threadMembers"][i] = {"onlineId": psn_id}
                ++i
        else:
            users_body["threadDetail"]["threadMembers"][0] = {"onlineId": psn_ids}

        users_body["threadDetail"]["threadMembers"][len(users_body["threadDetail"]["threadMembers"])] = {"onlineId": self.me}

        message = "\n"
        message += "--gc0p4Jq0M2Yt08jU534c0p\n"
        message += "Content-Type: application/json; charset=utf-8\n"
        message += "Content-Disposition: form-data; name=\"threadDetail\"\n"
        message += "\n"

        message += json.dumps(users_body) + "\n"

        message_body = {
            "messageEventDetail": {

                "messageDetail": {},
                "eventCategoryCode": message_type
            }
        }
        if (message_type == 1011):
            message_body["messageEventDetail"]["messageDetail"]["voiceDetail"]["playbackTime"] = audio_length

        message_body["messageEventDetail"]["messageDetail"]["body"] = message_text

        if (os.path.isfile(attachment)):
            attachment_content = attachment.bytes()
            attachment_length  = len(attachment_content)

        if (message_type == 1011):
            content_key = "voiceData"
            content_type = "audio/3gpp"
        elif (message_type == 3):
            content_key = "imageData"
            content_type = "image/jpeg"

        if (bool(attachment)):
            message += "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: ContentType\n"
            message += "Content-Disposition: form-data;name=\"" + content_key + "\"\n"
            message += "Content-Transfer-Encoding: binary\n"
            message += "Content-Length: AttachmentLength\n"
            message += "\n"

            message += attachment_content + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
        else:
            message += "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"

        s = requests.Session()
        s.mount(self.SEND_MESSAGE_URL+thread_id+"/messages", HTTP20Adapter())
        response = requests.Request('POST', self.SEND_MESSAGE_URL+thread_id+"/messages", headers=header, data=message)
        request = response.prepare()
        self.pretty_print_POST(request)
        '''

    def send_group_message(self, group_id, message_text = "", attachment = "", message_type = 1, audio_length = ""):
        header = {
            'Authorization': 'Bearer ' + self.oauth,
            'Content-Type': 'multipart/form-data; boundary="gc0p4Jq0M2Yt08jU534c0p"',
        }

        message_body = {
            "messageEventDetail": {
                "messageDetail": {

                },
                "eventCategoryCode": message_type
            }
        }
        if (message_type == 1011):
            message_body["messageEventDetail"]["messageDetail"]["voiceDetail"]["playbackTime"] = audio_length

        message_body["messageEventDetail"]["messageDetail"]["body"] = message_text

        if (os.path.isfile(attachment)):
            attachment_content = attachment.bytes()
            attachment_length  = strlen(attachment_content)

        if (message_type == 1011):
            content_key = "voiceData"
            content_type = "audio/3gpp"

        elif (message_type == 3):
            content_key = "imageData"
            content_type = "image/jpeg"

        if (bool(attachment)):
            message = "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: ContentType\n"
            message += "Content-Disposition: form-data;name=\"" + content_key + "\"\n"
            message += "Content-Transfer-Encoding: binary\n"
            message += "Content-Length: AttachmentLength\n"
            message += "\n"

            message += attachment_content + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
        else:
            message = "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
            response = requests.post(self.MESSAGE_THREADS_URL +  '/' + group_id + '/messages', headers=header, data=message).text

        return json.loads(response)

    def get_messages(self, group_id):
        header = {
            'Authorization': 'Bearer ' + self.oauth
        }
        url = self.MESSAGE_THREADS_URL + '/' + group_id + '?count=200&fields=threadMembers,threadNameDetail,threadThumbnailDetail,threadProperty,latestTakedownEventDetail,newArrivalEventDetail,threadEvents'
        response = requests.get(url, headers=header)
        data = json.loads(response.text)

        return data
