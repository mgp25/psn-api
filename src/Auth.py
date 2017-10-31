import simplejson
import json
import urllib.request
import urllib.parse
import os

class Auth:

    oauth = None
    last_error = None
    npsso = None
    grant_code = None
    refresh_token = None

    SSO_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/ssocookie'
    CODE_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize'
    OAUTH_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token'


    login_request = {
                        "authentication_type": 'password',
                        "username": None,
                        'password': None,
                        'client_id': '71a7beb8-f21a-47d9-a604-2e71bee24fe0'
                    }

    oauth_request = {
                        "app_context": "inapp_ios",
                        "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                        "client_secret": "zsISsjmCx85zgCJg",
                        "code": None,
                        "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
                        "grant_type": "authorization_code",
                        "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes"
                    }

    code_request = {
                        "state": "06d7AuZpOmJAwYYOWmVU63OMY",
                        "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
                        "app_context": "inapp_ios",
                        "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                        "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes",
                        "response_type": "code"
                    }

    refresh_oauth_request = {
                                "app_context": "inapp_ios",
                                "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                                "client_secret": "zsISsjmCx85zgCJg",
                                "refresh_token": None,
                                "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
                                "grant_type": "refresh_token",
                                "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes"
                            }

    two_factor_auth_request = {
                                "authentication_type": "two_step",
                                "ticket_uuid": None,
                                "code": None,
                                "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
                              }

    def __init__(self, email, password, ticket='', code=''):
        self.login_request['username'] = email
        self.login_request['password'] = password
        self.two_factor_auth_request['ticket_uuid'] = ticket
        self.two_factor_auth_request['code'] = code
        if (self.GrabNPSSO() is False or self.GrabCode() is False or self.GrabOAuth() is False):
            print('Error')


    def GrabNPSSO(self):
        if self.two_factor_auth_request['ticket_uuid'] and self.two_factor_auth_request['code']:
            data = urllib.parse.urlencode(self.two_factor_auth_request).encode('utf-8')
            request = urllib.request.Request(self.SSO_URL, data = data)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
        else:
            data = urllib.parse.urlencode(self.login_request).encode('utf-8')
            request = urllib.request.Request(self.SSO_URL, data = data)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
            if hasattr(data, 'error'):
                return False
            if hasattr(data, 'ticket_uuid'):
                error = {
                            'error': '2fa_code_required',
                            'error_description': '2FA Code Required',
                            'ticket': data['ticket_uuid']
                }
                self.last_error = json.dumps(error)
                return False
            self.npsso = data['npsso']
            return True

    def find_between(self, s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def GrabCode(self):
        data = urllib.parse.urlencode(self.code_request)
        url = self.CODE_URL+'?'+ data
        response = os.popen('curl -s -I -H \'Cookie: npsso='+self.npsso+'\' -X GET \''+url+'\' | grep -Fi X-NP-GRANT-CODE').readline()

        self.grant_code = self.find_between(response, 'X-NP-GRANT-CODE: ', '\n')

        if (self.grant_code is ''):
            error = {
                'error': 'invalid_np_grant',
                'error_description': 'Failed to obtain X-NP-GRANT-CODE',
                'error_code': 20
            }
            self.last_error = json.dumps(error)
            return False

        return True
    
    def GrabNewTokens(refreshToken):
        refresh_oauth_request = {
            "app_context": "inapp_ios",
            "client_id": "b7cbf451-6bb6-4a5a-8913-71e61f462787",
            "client_secret": "zsISsjmCx85zgCJg",
            "refresh_token": None,
            "duid": "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC",
            "grant_type": "refresh_token",
            "scope": "capone:report_submission,psn:sceapp,user:account.get,user:account.settings.privacy.get,user:account.settings.privacy.update,user:account.realName.get,user:account.realName.update,kamaji:get_account_hash,kamaji:ugc:distributor,oauth:manage_device_usercodes"
        }

        refresh_oauth_request['refresh_token'] = refreshToken

        data = urllib.parse.urlencode(refresh_oauth_request).encode('utf-8')
        request = urllib.request.Request('https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token', data = data)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))

        if hasattr(data, 'error'):
            return False

        return [data['access_token'], data['refresh_token']]

    def GrabOAuth(self):
        self.oauth_request['code'] = self.grant_code

        data = urllib.parse.urlencode(self.oauth_request).encode('utf-8')
        request = urllib.request.Request(self.OAUTH_URL, data = data)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))

        if hasattr(data, 'error'):
            self.last_error = data['body']
            return False

        self.oauth = data['access_token']
        self.refresh_token = data['refresh_token']

        return True

    def get_tokens(self):
        tokens = {
            "oauth": self.oauth,
            "refresh": self.refresh_token,
            "npsso": self.npsso
        }

        return tokens
