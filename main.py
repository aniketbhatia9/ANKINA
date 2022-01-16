import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sqlite3
import webbrowser
import time



listener = sr.Recognizer()
engine=pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command




def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song =command.replace('play','')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif "who are you" in command:
        talk("I am your virtual assistant created by Aniket")
    elif 'current time' in command:
        currenttime = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is '+currenttime)
        print('Current time is '+ currenttime)
    elif 'who is' in command:
        person = command.replace('who is','')
        info = wikipedia.summary(person,2)
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'connect' in command:
        database=command.replace('connect','')
        conn = sqlite3.connect(database+".db")
        print(conn)
    elif 'open' in command:
        f=open(command.replace('open','')+".txt","w+")
        talk("Do you want to enter data")
        choice=take_command()
        if 'yes' in choice:
            talk("What should I write sir")
            note=take_command()
            f.write(note)
    elif 'how are you' in command:
        talk("I am fine, Thank you")
    elif 'exit' in command:
        talk("Thanks for giving me your time")
        exit()
    elif 'timer' in command:
        def countdown(t):
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t -= 1
            print('Fire in the hole!!')
        # input time in seconds
        t = take_command()
        # function call
        countdown(int(t))
    elif "where is" in command:
        query = command.replace("where is", "")
        location = query
        talk("User asked to Locate")
        talk(location)
        webbrowser.open("https://www.google.nl / maps / place/" + location + "")
    else:
        talk('Please say the command again')

while True:
    run_alexa()

