import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import platform
import datetime
import time
import urllib.parse

# -------- Configuration ----------
WAKE_WORD = "assistant"     # set to None to always listen
EXIT_PHRASES = ("exit", "quit", "goodbye", "stop", "shut down")
# Map friendly app names to commands/paths (customize for your OS)
APP_COMMANDS = {
    "notepad": {"win": "notepad.exe", "mac": "open -a TextEdit", "linux": "gedit"},
    "calculator": {"win": "calc.exe", "mac": "open -a Calculator", "linux": "gnome-calculator"},
    "chrome": {"win": r"C:\Program Files\Google\Chrome\Application\chrome.exe", "mac": "open -a Google\\ Chrome", "linux": "google-chrome"},
}
# ----------------------------------

# init speech-to-text
recognizer = sr.Recognizer()
recognizer.energy_threshold = 400  # tweak if needed
recognizer.pause_threshold = 0.6

# init text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def open_app(app_name):
    system = platform.system().lower()
    entry = APP_COMMANDS.get(app_name)
    if not entry:
        speak(f"I don't have a path for {app_name}. Please update APP_COMMANDS.")
        return
    try:
        if system.startswith("windows"):
            path = entry.get("win")
            if path:
                os.startfile(path)
        elif system.startswith("darwin"):
            cmd = entry.get("mac")
            if cmd:
                subprocess.Popen(cmd, shell=True)
        else:
            cmd = entry.get("linux")
            if cmd:
                subprocess.Popen([cmd])
        speak(f"Opening {app_name}.")
    except Exception as e:
        speak(f"Failed to open {app_name}: {e}")

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def take_note(text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"note_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    speak(f"Saved note to {filename}")

def tell_joke():
    jokes = [
        "Why did the computer show up at work late? It had a hard drive.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings."
    ]
    speak(jokes[int(time.time()) % len(jokes)])

def open_news():
    webbrowser.open("https://news.google.com")
    speak("Opening news.")

def google_search(query):
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

def open_website(site):
    if not site.startswith("http"):
        site = "https://" + site
    webbrowser.open(site)
    speak(f"Opening {site}")

# Basic command parser
def handle_command(command):
    if not command:
        speak("I didn't catch that. Please repeat.")
        return False

    cmd = command.lower()
    print("Heard:", cmd)

    # Exit check
    if any(phrase in cmd for phrase in EXIT_PHRASES):
        speak("Goodbye!")
        return "exit"

    # Wake-word usage (if WAKE_WORD is set)
    if WAKE_WORD and WAKE_WORD not in cmd:
        # ignore non-wake words
        return None
    # If wake word present, remove it for easier parsing
    if WAKE_WORD and WAKE_WORD in cmd:
        cmd = cmd.replace(WAKE_WORD, "").strip()

    # Time
    if "time" in cmd:
        tell_time()
        return None

    # Open app
    if cmd.startswith("open "):
        target = cmd.replace("open ", "").strip()
        # if it's a website
        if "." in target or "http" in target:
            open_website(target)
            return None
        # else try to open as app
        open_app(target)
        return None

    # Google search
    if cmd.startswith("search ") or cmd.startswith("google "):
        # remove prefix
        query = cmd.split(" ", 1)[1]
        google_search(query)
        return None

    # Take note command: "note buy bread" or "take a note buy milk"
    if "note " in cmd or cmd.startswith("take note") or cmd.startswith("take a note"):
        # naive extraction:
        if "note" in cmd:
            idx = cmd.find("note")
            note_text = cmd[idx + len("note"):].strip()
            if not note_text:
                speak("What should I write in the note?")
                return None
            take_note(note_text)
            return None

    # Jokes
    if "joke" in cmd:
        tell_joke()
        return None

    # News
    if "news" in cmd:
        open_news()
        return None

    # Search websites like youtube
    if "youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        return None

    # Fallback: try a web search for the whole phrase
    google_search(cmd)
    return None

def listen_once(timeout=5, phrase_time_limit=6):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("Timeout waiting for phrase")
            return None
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("API unavailable:", e)
        return "REQUEST_ERROR"

def main_loop():
    speak("Voice assistant starting. Say 'assistant' before your command, or change WAKE_WORD to None to always listen.")
    while True:
        text = listen_once()
        if text == "REQUEST_ERROR":
            speak("Speech recognition service is unavailable. Check your internet connection.")
            time.sleep(2)
            continue
        result = handle_command(text)
        if result == "exit":
            break
        # slight pause to avoid recognizing the assistant's own speech
        time.sleep(0.3)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        speak("Shutting down. Bye!")
