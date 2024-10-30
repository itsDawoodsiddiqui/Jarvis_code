import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musiclibrary
from gtts import gTTS
import pygame

r = sr.Recognizer()  # Use `r` consistently
engine = pyttsx3.init()  # Initialize pyttsx3 engine
newsapi = "ccd154be70cf44aebb76629eda9b81be"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with your file path

    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait for the music to finish
    while pygame.mixer.music.get_busy():  # Returns False when music is done playing
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")
   
        

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com") 
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]  # Get song name after 'play'
        if song in musiclibrary.music:
            link = musiclibrary.music[song]  # Get song link
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=pak&apiKey={newsapi}")
        
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            
            for article in articles:
                speak(article['title'])  
    else:
        pass              



if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening...!")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")

                with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error:", format(e))
