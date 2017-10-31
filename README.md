# PSN API
<img src="http://vignette1.wikia.nocookie.net/logopedia/images/7/7e/PlayStation_Network.png/revision/latest?cb=20110901131500" height="50">

This is a python wrapper for the PSN API.

**Read the [wiki](https://github.com/mgp25/psn-api/wiki)** and previous issues before opening a new one! Maybe your issue is already answered.

**Do you like this project? Support it by donating**
- ![Paypal](https://raw.githubusercontent.com/reek/anti-adblock-killer/gh-pages/images/paypal.png) Paypal: [Donate](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=FX7YLU6SX8ZZ6)
- ![btc](https://camo.githubusercontent.com/4bc31b03fc4026aa2f14e09c25c09b81e06d5e71/687474703a2f2f7777772e6d6f6e747265616c626974636f696e2e636f6d2f696d672f66617669636f6e2e69636f) Bitcoin: 1DCEpC9wYXeUGXS58qSsqKzyy7HLTTXNYe

## How to get refresh token

Sony now is using reCaptcha. There is no way to do this authentication via the Script at this time. So we have worked around the authentication issue by doing the following.

1. From the PSN Website or App or Console Enable 2 Step Verification
2. Go to [https://auth.api.sonyentertainmentnetwork.com/login.jsp](https://auth.api.sonyentertainmentnetwork.com/login.jsp) Enter your credentials, Solve the reCaptcha, and when you get the `ENTER Verification Code` screen take a look at the URL in your browser. Collect the following ID: `ticket_uuid=b7aeb485-xxxx-4ec2-zzzz-0f23bcee5bc5&layout_type=......` **DO NOT ENTER THE VERIFICATION CODE**
3. From the API

```python
auth = Auth('YOUR EMAIL', 'YOUR PASSWORD', b7aeb485-xxxx-4ec2-zzzz-0f23bcee5bc5, 'verification_code_you_got_on_your_phone)

tokens = auth.get_tokens()

print(tokens)
```

4. Save the `refresh` and `npsso` values from the output

5. From now on you can authenticate (Refresh your tokens) instead of re-authenticating every time.

Like this:

```python
new_token_pair = Auth.GrabNewTokens(refresh_token)

tokens = {
    "oauth": new_token_pair[0],
    "refresh": new_token_pair[1],
    "npsso": npsso # saved above!
}

friend = Friend(tokens)
friend_list = friend.my_friends()
```

## Features
- Login to PSN
- Get user information
- View and manage your friends list
- Manage and send messages through PSN

## TODO
- View trophies and trophies for a specific game
- Create, manage and view communities

## Legal

This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by PlayStation or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.
