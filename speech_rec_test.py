import speech_recognition as sr
import pyaudio
import json
import clashroyale
import globals

globals.init()

# get list of cards
officialClient = clashroyale.official_api.Client(globals.officialAPIToken)
list_of_cards = [x.name.replace(".", "").lower() for x in officialClient.get_all_cards()]
print(list_of_cards)


def find_card_spoken(words, list_of_cards):
    for word in words:
        if word in list_of_cards:
            print(word)
            return word
    return ""


# initialize the recognizer
r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    r.adjust_for_ambient_noise(source)
    while True:
        # read the audio data from the default microphone
        print('speak!')
        audio_data = r.listen(source, timeout=0)
        # print("Recognizing...")```````
        # convert speech to text
        try:
            # text = r.recognize_google(audio_data)
            text = r.recognize_google(audio_data, show_all=True)
            words = [x['transcript'].lower() for x in text['alternative']]
            print(text)
            print(words)
            card_spoken = find_card_spoken(words, list_of_cards)
        except:
            text = ""
            words = []
            card_spoken = ""
        if card_spoken == "" and "quit" in words:
            quit()
