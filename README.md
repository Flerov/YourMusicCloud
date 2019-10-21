# YourMusicCloud
Tired of paying money for streaming services? I got your back. 

This app is build on top of flask and uses spotify-dowloader to easily download spotify tracks over youtube

This is a alpha version that I have made for fun and without any planing! So the code structure could definitly be better.
There will also come many futures.

What you currently can: 
+ Submit a song as a string, but be sure that the song is written correctly and available on youtube since the first result matching your input will be downloaded
+ Submit a spotify/youtube track link in the following format > 'spotify:track:<someuid>' (You can get that link from spotify)
  That track will asynchroniously be downloaded and added to your standard 'Music' folder
+  All the futures provided by 'spotify-downloader' (most have to come in further updates)
  
What you will be able to do after I update this repository:
+ Submit a album and artist name to download the whole album
+ Submit a youtube playlist link to get them songs
+ Submit a spotify playlist link to get them song

* using wsgi test environment (if you want to use production server change it yourself in flask-app.py file)
Run 'python flask-app.py' to start the web server
Access webpage:
IP: 0.0.0.0
Port: 50000
(Link: http://0.0.0.0:5000)

!Tip: change localhost to your local ip to call webpage from all devices connected in your network like phone, tablet, pc

![Alt text](https://github.com/Flerov/YourMusicCloud/blob/pictures/web-app.png)
