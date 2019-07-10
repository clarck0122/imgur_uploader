# imgur_uploader



upload cute girl image form [Beauty board](https://www.ptt.cc/bbs/index.html/)
to [imgur](https://imgur.com/a/8y0utle/).(**This is Final Result**)



## Run in local machine 

#### 1. [Sign up account](https://imgur.com/)
![alt tag](https://i.imgur.com/RiqQcON.png)


#### 2. Create Album and get Album ID
![alt tag](https://i.imgur.com/DWVrkpV.png)
![alt tag](https://i.imgur.com/O15Aqpx.png)
![alt tag](https://i.imgur.com/795KxSV.png)


#### 3. [Create App](https://api.imgur.com/oauth2/addclient)
![alt tag](https://i.imgur.com/ZZyL4gh.png)


#### 4. Get app ClientID and Client_Secret
![alt tag](https://i.imgur.com/o8KD2br.png)


#### 5. Get Access token and Refresh token
- Edit auth.py
```
self.client_id = # YOUR ClientID
self.client_secret = # YOUR Client_Secret
```
- and run
```
python auth.py
```
- go to web url in terminal
![alt tag](https://i.imgur.com/ZRtnEJB.png)
- get pin code and enter pin code

#### 6. Setup uploader
- Edit uploader.py
```
self.client_id = # YOUR ClientID
self.client_secret = # YOUR Client_Secret
self.access_token = # YOUR access_token
self.refresh_token = # YOUR refresh_token
self.album_id = # YOUR Album_ID   
```
    
#### 7. execute Main Process
```
python app.py
```
