#Virtual Assistant
#A smart assistant that responds to user commands  to open apps or to search any information.


import pyttsx3  
import speech_recognition as sr  
import webbrowser
import os
import pywhatkit as kit
import pyautogui


screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")
print("Screenshot saved!")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  


def speak(audio):
    print(f"Speaking: {audio}")  
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Audio captured")  
        except sr.WaitTimeoutError:
            print("Timeout waiting for audio")
            return "None"
        except Exception as e:
            print(f"Error capturing audio: {e}")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "None"
    except Exception as e:
        print(f"Error recognizing audio: {e}")
        return "None"

def openWebsite(url):
    try:
        webbrowser.open(url)
        speak(f"ok")
    except Exception as e:
        print(f"Error opening {url}: {e}")
        speak(f"Sorry, I couldn't open {url}")

def playMusic(music_dir):
    try:
        if os.path.exists(music_dir):
            songs = [file for file in os.listdir(music_dir) if file.endswith(('.mp3', '.wav'))]
            if songs:
                print(f"Found songs: {songs}")
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music")
            else:
                speak("No compatible music files found in the directory")
        else:
            speak("The specified music directory does not exist")
    except Exception as e:
        print(f"Error playing music: {e}")
        speak("Sorry, I couldn't play music")

def searchGoogle(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query} on Google")
    except Exception as e:
        print(f"Error performing Google search for {query}: {e}")
        speak(f"Sorry, I couldn't search for {query}")
        

if __name__ == "__main__":
    speak("Hey, I'm Ellis. How can I help you?")
    
    while True:
        query = takeCommand()

        if query == "None":
            continue

        if 'open youtube' in query:
            openWebsite("https://www.youtube.com")

        elif 'open google' in query:
            openWebsite("https://www.google.com")

        elif 'open pinterest' in query:
            openWebsite("https://in.pinterest.com/")


        elif 'play' in query:
         video = query.replace("play", "").strip()
         if video:
          speak(f"Playing {video} on YouTube")
          kit.playonyt(video)
         else:
          speak("What do you want me to play?")

        elif 'play song' in query:
         speak("Which song would you like me to play?")
        song_query = takeCommand().lower()
        if song_query != "None":
                speak(f"Playing {song_query} on YouTube")
                kit.playonyt(song_query)
        
        elif 'search' in query:
            search_query = query.replace("search", "").strip()
            if search_query:
                searchGoogle(search_query)
            else:
                speak("What do you want to search for?")
                search_query = takeCommand().lower()
                if search_query != "None":
                    searchGoogle(search_query)
        
        elif 'take screenshot' in query:
           speak("Taking screenshot")
           screenshot = pyautogui.screenshot()
           screenshot.save("screenshot.png")
           speak("Screenshot saved")



        else:
            print("No query matched")
