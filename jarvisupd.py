import pyttsx3
import speech_recognition as sr
import os
import pyautogui
import time
import webbrowser as br
# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use the male voice
engine.setProperty('rate', 170)  # Set speaking rate
engine.setProperty('volume', engine.getProperty('volume') + 0.25)  # Increase volume slightly

def speak(audio):
    """Speak the given text."""
    engine.say(audio)
    engine.runAndWait()

def greet():
    """Greet the user."""
    speak("Hi Sir, how can I help you?")
def closetab():
    """Simulate the keyboard shortcut to close the current browser tab."""
    speak("Closing the current tab.")
    pyautogui.hotkey('ctrl', 'w')  # Use 'command' instead of 'ctrl' for macOS
    time.sleep(0.5)  # Add a short delay for smooth operation
def openyt():
    speak("opening youtube")
    br.open("https://www.youtube.com/")
def leet():
    br.open("https://www.leetcode.com")
def open(query):
    query=query.replace("open","").strip()
    pyautogui.press("super")
    pyautogui.typewrite(query)
    pyautogui.sleep(2)
    pyautogui.press("Enter")

def search(query):
    """Search the web browser for the given query."""
    if "search for" in query:
        query = query.replace("search for", "").strip()
    elif "search" in query:
        query = query.replace("search", "").strip()
    else:
        query = query.strip()
    
    if query:
        speak(f"Searching for {query}")
        br.open(f"https://www.google.com/search?q={query}")
    else:
        speak("Please tell me what to search for.")
def command():
    """Listen for a voice command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust to ambient noise
        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)
            print("Understanding...")
            query = recognizer.recognize_google(audio, language='en-in')  # Use recognize_google
            print(f"You said: {query}\n")
        except sr.UnknownValueError:
            speak("I didn't catch that. Please say that again.")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition; {e}")
            return "None"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "None"
    return query

if True:
    while True:
        user_query = command().lower()
        if "wake up" in user_query:
            greet()
        elif "open youtube" in user_query:
             openyt()
        elif "leet code" in user_query:
              leet()
        elif "search" in user_query:
            search(user_query)
        elif "close tab" in user_query:
            closetab()
        elif "open" in user_query:
            open(user_query)
        elif "exit" in user_query or "bye" in user_query:
            speak("Goodbye, Sir!")
            break
