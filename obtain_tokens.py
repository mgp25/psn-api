from psnapi.Auth import Auth
from psnapi.Friend import Friend
from psnapi.User import User
from psnapi.Messaging import Messaging
import json

auth = Auth('YOUR_EMAIL', 'YOUR_PASSWORD', 'TICKET_UUID', '2FA')

tokens = auth.get_tokens()

f = open('tokens', 'wt', encoding='utf-8')
f.write(json.dumps(tokens))
f.close()

print('Your tokens have been saved in the file \'tokens\'')
