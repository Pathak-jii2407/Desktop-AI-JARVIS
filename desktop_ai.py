import pyttsx3
import speech_recognition as sr
import random
import wikipedia
import webbrowser as wb
import smtplib
import datetime
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()

    except Exception as e:
        print("Say that again please...")
        return "None"

def sendEmail():
    try:
        speak("Please provide the email details.")
        speak("Recipient email address:")
        to_email = input("Recipient email address: ")
        speak(f"Sending email to {to_email}. What should be the subject?")
        subject = input("Subject: ")
        speak("What should be the email message?")
        message = input("Message: ")
        email_address = "ved24072003@gmail.com"
        password = 'llaf fnvt mmta cydj'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, password)

        email_content = f"Subject: {subject}\n\n{message}"

        server.sendmail(email_address, to_email, email_content)
        server.quit()

        speak("Email sent successfully.")

    except Exception as e:
        speak("Sorry, I couldn't send the email.")
def setReminder():
    speak("Sure, please tell me what do you want to be reminded of?")
    reminder_text = takeCommand()

    if 'none' not in reminder_text:
        speak("When do you want me to remind you?")

        while True:
            reminder_time = takeCommand()
            if 'none' in reminder_time:
                speak("Okay, no problem.")
                return
            try:
                reminder_datetime = datetime.datetime.strptime(reminder_time, '%H:%M')
                current_time = datetime.datetime.now().strftime('%H:%M')

                delta = (reminder_datetime - datetime.datetime.now()).seconds
                print(f"Reminder set for {reminder_time}. I will remind you in {delta // 60} minutes.")
                speak(f"Reminder set for {reminder_time}. I will remind you in {delta // 60} minutes.")
                break
            except ValueError:
                speak("I couldn't understand the time. Please provide the time in the HH:MM format.")

def calculator(query):
    try:
        expression = query.replace('calculate', '').replace('into','*').replace('x','*').strip()
        result = eval(expression)
        speak(f"The result is {result}")

    except Exception as e:
        speak("Sorry, I couldn't calculate that.")

def Jarvis():
    query = takeCommand().lower()

    if 'friday' in query:
        engine.setProperty('voice', voices[1].id)
        friday_responses = [
            "Yes boss", "I woke up", "Sorry sir, I was sleeping",
            "I am listening", "What can I do for you", "Present boss"
        ]
        friday_choose = random.choice(friday_responses)
        speak(friday_choose)

    elif 'wikipedia' in query:
        search_results = wikipedia.summary(query, sentences=3)
        print(search_results)
        speak(search_results)

    elif 'google' in query:
        search_query = query.replace('google', '').replace('search','').strip()
        search_url = f'https://www.google.co.in/search?q={search_query}'
        wb.open_new(search_url)
        speak('opening')

    elif 'send email' in query:
        sendEmail()

    elif 'set reminder' in query:
        setReminder()
    
    elif 'calculate' in query:
        calculator(query)
    
    elif 'youtube' in query:
        query=query.replace('search','').replace('play','').replace('youtube','')
        search_url="https://www.youtube.com/results?search_query="+query
        wb.open_new(search_url)

    elif 'close' in query:
        speak('Ok Boss')
        exit()
    
while True:
    Jarvis()
