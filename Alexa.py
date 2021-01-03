import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia


listener = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

talk('I am  your listener')
talk("How can I help you")

def my_commands():
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if 'gayathri' in command:
                command = command.replace("gayathri",'')
                print(command)
    except:
        pass
    return command

def run():
    command = my_commands()

    if 'play' in command:
       song_name = command.replace('play', '')
       talk('playing' + song_name)
       pywhatkit.playonyt(song_name)
       print(song_name)

    elif 'search' in command:
         search = command.replace('search','')
         talk('searching' + search)
         pywhatkit.search(search)
         print(search)

    elif 'time' in command:
        date_time = datetime.datetime.now().strftime('%I %M %p')
        print(date_time)
        talk('Current time is' + date_time)

    elif 'date' in command:
        date_time = datetime.datetime.now().strftime('%d %B %A')
        print(date_time)
        talk('Date is' + date_time)

    elif 'who' in command:
        search = command.replace('who', '')
        info = wikipedia.summary(search, 1)
        print(info)
        talk(info)

    elif 'send' in command:
        send = command.replace('send','')
        talk('sending the message')
        pywhatkit.sendwhatmsg('+91 9003555635','sending msg via python',19,13)
        print('message sent')

    else:
        talk('please say it again')

run()

while True:
    run()