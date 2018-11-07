# imgur_uploader
upload file to imgur form Beauty board https://www.ptt.cc/bbs/index.html


1. regist imgur account 

2. Create an Album, and get its Album ID

2. get Client_ID and Client_Secret 

    https://api.imgur.com/#registerapp

    support Authorization type chose the following option

        OAuth 2 authorization without a callback URL

3. run python3 auth.py to get access_token and refresh_token

4. export Client_ID, Client_Secret, access_token, refresh_token, Album_ID to environment variable

5. finally, run upload.py