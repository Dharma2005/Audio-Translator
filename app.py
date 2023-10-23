from flask import Flask, render_template, request
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from translate import Translator
import os

app = Flask(__name__)

# Define a global variable to store the filename
filename = ""

# Define the route for the home page
@app.route('/')
@app.route('/register')
def index():
    return render_template('register.html')

# Define the route for file upload and audio translation
@app.route('/upload', methods=['POST'])
def upload():
    global filename

    file = request.files['file']
    if file and file.filename.endswith('.wav'):
        filename = os.path.join( 'static', 'r5.wav')
        file.save(filename)
        translation = convert_audio(filename)
        return render_template('register.html', translation=translation)
    else:
        return render_template('register.html')

def convert_audio(sound):
    r = sr.Recognizer()
    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        print("Converting audio...")
        audio = r.record(source)
        try:
            Text = r.recognize_google(audio)
            print("Converted audio is:")
            print(Text)
            translator = Translator(to_lang="te")
            translation = translator.translate(Text)
            print(translation)
            # Use gTTS to generate an audio file with the translated text
            tts = gTTS(text=translation, lang="te")
            translated_audio_path = os.path.join( 'static', 'r5.mp3')
            tts.save(translated_audio_path)
            return translation
        except sr.UnknownValueError:
            print("Error: audio could not be recognized")
            return None
        except sr.RequestError as e:
            print("Error: Could not request results; {0}".format(e))
            return None

if __name__ == '__main__':
    app.run(debug=True)
