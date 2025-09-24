#Author: Aaron M. Leonhard
#Date: 09:21:2025
#Description: This program uses a speech recognition library and VOSK to receive commands through a microphone. Keywords listed below:
#"time" Get the time
#"date" Get the date
#"rick" Get rick rolled
#"song + <songName>" Starts the song with that name if it's in the folder
#"playlist" Starts the playlist
#"radio + (Jazz, Electro, Trance, Christian, Disco)" Starts the radio *Requires internet connection

import speech_recognition as sr
from pathlib import Path
import time

#OPTIONAL IMPORTS
try:
    from mutagen.mp3 import MP3
    from mutagen.mp4 import MP4
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False
try:
    import vlc
    VLC_AVAILABLE = True
except ImportError:
    VLC_AVAILABLE = False



songFolderPath = "C:\\Users\\Owner\\Desktop\\Musics"



def playVLCMP3(song):
    print("parsing song...")
    instance = vlc.Instance('--aout=directsound')

    player = instance.media_player_new()
    media = instance.media_new(song)
    duration_ms = MP3(song).info.length
    player.set_media(media)
    player.play()
    time.sleep(duration_ms)
    player.stop()

def playVLCMP4(song):
    print("parsing file...")
    instance = vlc.Instance('--aout=directsound')

    player = instance.media_player_new()
    media = instance.media_new(song)
    duration_ms = MP4(song).info.length
    player.set_media(media)
    player.play()
    time.sleep(duration_ms)
    player.stop()

def playVLCStream(streamPath):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(streamPath)
    player.set_media(media)
    player.play()
    time.sleep(2)
    try:
        while True:
            state = player.get_state()
            if state == vlc.State.Ended or state == vlc.State.Error:
                print(f"Stream ended or error: {state}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stream has been cancelled")
    player.stop()
    player.release()
    instance.release()
    print("exiting thread 2")

#def getAllPlaylists():
def getAllSongs():
    songNamesAndPaths = []
    folder_path = Path("C:\\Users\\Owner\\Desktop\\Music to vibe")
    for f in folder_path.iterdir():
        if f.is_file():
            songNameAndPath = (f.with_suffix('').name.lower(), f)
            songNamesAndPaths.append(songNameAndPath)
    print(songNamesAndPaths)
    return songNamesAndPaths

def playVLCPlaylist(playlistPath):
    print("parsing playlist...")
    instance = vlc.Instance()

    media = instance.media_new(playlistPath)
    media.parse()
    time.sleep(5) #wait for the parsing

    media_list = media.subitems()
    if media_list.count() > 0:
        list_player = instance.media_list_player_new()
        list_player.set_media_list(media_list)
        list_player.play()
        
        try:
            while True:
                state = list_player.get_state()
                if state == vlc.State.Ended:
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
        list_player.stop()
        list_player.release()
        list_player = None
    else:
        print("No items found in playlist or parsing failed")

def processInput(r):
    endProgram = False
    radioStationString = None
    allSongs = getAllSongs()
    while(not endProgram):
        try:
            with sr.Microphone() as source2:
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print(MyText)
            if("end" in MyText or "exit" in MyText):
                exit()
            # Will use a small GUI for this:
            # elif("stop" in MyText):
            #     radioStationString = None
            elif("time" in MyText):
                currentTime = time.localtime()
                formatedTime = time.strftime("%I:%M", currentTime)
                print(formatedTime)
            elif("date" in MyText):
                currentTime = time.localtime()
                formatedTime = time.strftime("%B %d, %Y", currentTime)
                print(formatedTime)
            #outside the 'with' statement
            if(VLC_AVAILABLE and MUTAGEN_AVAILABLE):
                if("rick" in MyText):
                    playVLCMP4('C:\\Users\\Owner\\Desktop\\Musics\\Never Gonna Give You Up.m4a')
                elif("playlist" in MyText):
                    playVLCPlaylist('C:\\Users\\Owner\\Desktop\\Musics\\coolPlaylist.xspf')
                elif("radio" in MyText):
                    if("christian" in MyText):
                        radioStationString = "https://maestro.emfcdn.com/stream_for/k-love/web/aac"
                    elif("jazz" in MyText):
                        radioStationString = "http://bobcatradio.hisd.com:8000/main"
                    elif("electro" in MyText):
                        radioStationString = "https://stream.bigfm.de/edm/mp3-128/"
                    elif("disco" in MyText):
                        radioStationString = "https://antares.dribbcast.com/proxy/s8190/stream"
                    elif("trance" in MyText):
                        radioStationString = "https://s3.slotex.pl:7252/;"

                    if(radioStationString != None):
                        playVLCStream(radioStationString)
                    
                if("song" in MyText):
                    for songName, songPath in allSongs:
                        if(songName in MyText):
                            playVLCMP4(songPath)
                #include mp3 access

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("I didn't understand that.")
        except AttributeError:
            print("An error occurred! Please make sure your microphone is enabled!")
            exit()
    return MyText

def main():
    r = sr.Recognizer() 
    processInput(r)

if __name__ == '__main__':
    main()