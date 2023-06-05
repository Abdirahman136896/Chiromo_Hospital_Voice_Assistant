from neuralintents import GenericAssistant
from datetime import date
import os.path
import speech_recognition
import pyttsx3
import sys

#setting up a recognizer which is the speech recognition.we need to initialize the speaker and then create the assistant
recognizer = speech_recognition.Recognizer()

speaker = pyttsx3.init()
speaker.setProperty('rate', 150) #depending on how fast the assistant should talk

#we are going to have an object which is the actual todolist
services_offered = ['Covid vaccination', 'Pediatrics', 'Gynecology', 'Specialist consulting clinics', 'Dentist', 'Laboratory', 'Pharmacy', 'X-rays and ultrasounds', 'Ambulance services']

todo_list = ['Go shopping', 'Clean Room', 'Record Video']

def create_note():
    global recognizer

    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you!Please try again")
            speaker.runAndWait()

def book_service():
    print(services_offered)

    global recognizer

    speaker.say("Which of our below indicated services would you like today?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                serv = recognizer.recognize_google(audio)
                serv = serv.lower()

                #speaker.say("Choose a filename!")
                #speaker.runAndWait()

                # recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                # audio = recognizer.listen(mic)

                filename = date.today()
                name = input("What is the patients name?")
                #name = "Abdul"

                t = filename.strftime('%m/%d/%Y')

                print(t + "\n")
                print(type(t))

                exst = os.path.exists(t)

                print(exst)

                speaker.say("Any comments to be added to your service booking?")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                commnt = recognizer.recognize_google(audio)






                #if (exst == True):
                with open(name, 'a') as f:
                        f.write(serv + " - " + t + " - " + commnt + "\n")
                        f.close()
                        done = True
                        print("File created is: " + name)
                        speaker.say(f"I successfully created and updated the new service for patient name: {name}")
                        speaker.runAndWait()

                #else:
                    #with open(t, 'x') as f:
                        #f.write(name + " - " + serv + "\n")
                        #f.close()
                        #done = True
                        #speaker.say(f"I successfully created the note {filename}")
                        #speaker.runAndWait()
                        #print("File created is: " + t)


        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you!Please try again")
            speaker.runAndWait()


def add_service():

    global recognizer

    speaker.say("What service do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                services_offered.append(item)
                done = True

                speaker.say(f"I added {item} to the to do list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you!Please try again")
            speaker.runAndWait()

def show_services():

    speaker.say("The services offered by chiromo hospital are the following")
    print(services_offered)
    for item in services_offered:
        speaker.say(item)
    speaker.runAndWait()

#def service_list():

    #speaker.say("The services offered by chiromo hospital are the following")
    #for element in services_offered:
        #speaker.say(element)
    #speaker.runAndWait()

def hello():
    speaker.say("Hello. What can I do for you?")
    speaker.runAndWait()

def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    'greeting': hello,
    'book_service': book_service,
    'add_service': add_service,
    'show_services': show_services,
    'exit': quit
}


assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:

    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
