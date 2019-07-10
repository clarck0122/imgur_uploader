# imgur_uploader



upload cute girl image to [imgur](https://imgur.com/a/8y0utle/).
form [Beauty board](https://www.ptt.cc/bbs/index.html/).



## 1. Imgur Account 

1. [Sign up account](https://imgur.com/)

2. Create Album and get Album ID

3. [Create App](https://api.imgur.com/oauth2/addclient)

5. Get app ClientID and Client_Secret

6. Get Access token and Refresh token
- Edit auth.py
```
self.client_id = #YOUR ClientID
self.client_secret = #YOUR Client_Secret
```
- and run
```
python auth.py
```
- go to web url in terminal

- get pin code and enter pin code





2. Create an Album, and get its Album ID

2. get Client_ID and Client_Secret 

    https://api.imgur.com/#registerapp

    support Authorization type chose the following option

        OAuth 2 authorization without a callback URL

3. run python3 auth.py to get access_token and refresh_token

4. export Client_ID, Client_Secret, access_token, refresh_token, Album_ID to environment variable

5. finally, run upload.py
