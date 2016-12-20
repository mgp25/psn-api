from src.Auth import Auth
from src.Friend import Friend
from src.User import User
from src.Messaging import Messaging

auth = Auth('YOUR EMAIL', 'YOUR PASSWORD')
tokens = auth.get_tokens()

friend = Friend(tokens)
friend_list = friend.my_friends()

friend_string = ''
if bool(friend_list):
    for key, value in friend_list.items():
        friend_string += key+' is playing '+value+"\n"
else:
    friend_string = 'No friends online'

print(friend_string)
