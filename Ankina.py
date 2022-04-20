#importing libraries
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sqlite3
import webbrowser
import time
import pyautogui
import os
import random
import requests
import wolframalpha
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from AnkinaUI import Ui_AnkinaUI

#ANKINA VOICE BOT VERSION 1.0
#APP DEVELOPERS :-
#ANIKET BHATIA
#ANKIT GARG
#JOVINA JACINTA CASTELINO
#AAN SARAH ZACHARIAH


#Setting up Voice Command Input
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-1].id)
engine.setProperty('rate', 170)

#Speak Command
def talk(text):
    engine.say(text)
    engine.runAndWait()


#Wish Me Command
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 5 and hour <= 12:
        print("Good Morning Sir")
        talk('Good Morning Sir')
        print("I am Ankina Version 1.0 , How can I help You")
        talk("I am Ankina Version 1.0 , How can I help You")
    elif hour > 12 and hour < 17:
        print("Good Afternoon Sir")
        talk('Good Afternoon Sir')
        print("I am Ankina Version 1.0 , How can I help You")
        talk("I am Ankina Version 1.0 , How can I help You")
    else:
        print("Good Evening Sir")
        talk("Good Evening Sir")
        print("I am Ankina Version 1.0 , How can I help You")
        talk("I am Ankina Version 1.0 , How can I help You")




#MainThread class with init function
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()


#Microphone Input Command

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            text = r.listen(source)
        try:
            print("Recognizing...")
            command = r.recognize_google(text, language='en-in')
            print(f"user said: (command)")
        except Exception as e:
            return "none"
        command = command.lower()
        return command


#All the task commands
    def TaskExecution(self):
        wish()
        while True:
            self.command = self.take_command()
            print(self.command)


            #Youtube Play Command
            if 'play' in self.command:
                song = self.command.replace('play', '')
                talk('playing' + song)
                pywhatkit.playonyt(song)

            #Who are You Command
            elif "who are you" in self.command:
                print("I am your virtual assistant created by Aniket")
                talk("I am your virtual assistant created by Aniket")

            #Current Time Display Command
            elif 'current time' in self.command:
                currenttime = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + currenttime)
                print('Current time is ' + currenttime)


            #Display News In Browser Command
            elif 'news' in self.command:
                news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
                talk('Here are some headlines from the Times of India,Happy reading')

            #Ask Me Command
            elif 'ask' in self.command:
                talk('I can answer to computational and geographical questions and what question do you want to ask now')
                question = self.take_command()
                app_id = "R2K75H-7ELALHR35X"
                client = wolframalpha.Client('R2K75H-7ELALHR35X')
                res = client.query(question)
                answer = next(res.results).text
                talk(answer)
                print(answer)

            #Display Weather by taking the city name as Input through voice command
            elif "weather" in self.command:
                api_key = "ba5428d67e3e380a0d85006c411543a5"
                base_url = "https://api.openweathermap.org/data/2.5/weather?"
                talk("whats the city name")
                city_name = self.take_command()
                print("city_name")
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    talk(" Temperature in kelvin unit is " +
                         str(current_temperature) +
                         "\n humidity in percentage is " +
                         str(current_humidiy) +
                         "\n description  " +
                         str(weather_description))
                    celsius = current_temperature - 273.15
                    print(" Temperature in kelvin unit = " +
                          str(current_temperature) +
                          "\n Temperature in celsius = " +
                          str(celsius) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))

                else:
                    talk(" City Not Found ")

            #Who is Command
            elif 'who is' in self.command:
                person = self.command.replace('who is', '')
                info = wikipedia.summary(person, 2)
                print(info)
                talk(info)

            #Tell me a joke Command
            elif 'joke' in self.command:
                print(pyjokes.get_joke())
                #talk(pyjokes.get_joke())

            #Database Connectivity Command
            elif 'connect' in self.command:
                database = self.command.replace('connect', '')
                conn = sqlite3.connect(database + ".db")
                print(conn)

            #Take a note Command
            elif 'open' in self.command:
                f = open(self.command.replace('open', '') + ".txt", "w+")
                talk("Do you want to enter data")
                choice = self.take_command()
                if 'yes' in choice:
                    talk("What should I write sir")
                    note = self.take_command()
                    f.write(note)
                    f.close()

            #How are you Command
            elif 'how are you' in self.command:
                talk("I am fine, Thank you")

            #Sign off Command
            elif 'exit' in self.command:
                 talk("Thanks for giving me your time")
                 exit()

            #Start a Timer Command
            elif 'timer' in self.command:
                def countdown(t):
                    while t:
                        mins, secs = divmod(t, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        t -= 1
                    print('Fire in the hole!!')

                # input time in seconds
                t = self.take_command()
                # function call
                countdown(int(t))

            #To find a place Command
            elif "where is" in self.command:
                query = self.command.replace("where is", "")
                location = query
                talk("User asked to Locate")
                talk(location)
                webbrowser.open("https://www.google.co.in/maps/place/" + location )

            #Start Music Command
            elif "start music" in self.command:
                music_dir = "E:\\Music"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            #Volume Controls Commands
            elif "volume up" in self.command:
                pyautogui.press("volumeup")
            elif "volume down" in self.command:
                pyautogui.press("volumedown")
            elif "volume mute" in self.command or "mute" in self.command:
                pyautogui.press("volumemute")

            #Open Facebook
            elif "show facebook" in self.command:
                webbrowser.open("www.facebook.com")

            #Open Instagram
            elif "show instagram" in self.command:
                webbrowser.open("www.instagram.com")

            #Search Command
            elif "search" in self.command:
                print("What should I search for you?")
                talk("What should I search for you?")
                cm = self.take_command().lower()
                webbrowser.open(f"{cm}")

            #Send a Message on whatsapp Command
            elif "send message" in self.command:
                talk("Enter the number")
                number=input("Enter the number")
                talk("Enter the message")
                message=input("Enter the message")
                talk("Enter the hour")
                hr=int(input("Enter the hour"))
                talk("Enter the minute")
                min=int(input("Enter the minute"))
                print(number)
                print(message)
                print(hr)
                print(min)
                pywhatkit.sendwhatmsg(number, message, hr, min)
                print("Done")

            #What is my IP Address Command
            elif "ip address" in self.command:
                from requests import get

                ip = get('https://api.ipify.org').text
                talk(f"your IP address is {ip}")
                print(ip)

            #Open Notepad Command
            elif "notepad" in self.command:
                npath = "c:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            #None of the above
            else:
                talk('Please say the command again')


#Define MainWindow Class
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_AnkinaUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

#GUI define
    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Ankina/__02-____.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Ankina/OccasionalBonyDugong-size_restricted.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

#Show Time on Main Window
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

#Start Execution
startExecution = MainThread()

#System Define
app = QApplication(sys.argv)
Ankina = Main()
Ankina.show()
sys.exit(app.exec_())

