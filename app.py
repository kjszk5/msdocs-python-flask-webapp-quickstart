from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import azure.cognitiveservices.speech as speechsdk
import os

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')
   COG_SERVICE_KEY="f475a189ffdd4362bfa09715ebc73660"
   COG_SERVICE_REGION="japaneast"
   config = speechsdk.SpeechConfig(subscription = COG_SERVICE_KEY,region = COG_SERVICE_REGION)
#   config.speech_recognition_language="en-US"
#   config.enable_dictation()
#   audio_config = speechsdk.AudioConfig(use_default_microphone=True)
   print('speech serviceのregionはこちらに設定しました:', config.region)
   reference_text="I got a cold call from an insurance company yesterday."
   audioFile = 'bbb.wav'
   audio_config = speechsdk.AudioConfig(filename=audioFile)
#   audio_config = speechsdk.AudioConfig(use_default_microphone=True)

   pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=reference_text,grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,enable_miscue=True)
   print("TEST1")
   print(os.path.abspath(__file__))
   print(os.path.abspath(audioFile))
   try:
#       speech_recognizer = speechsdk.SpeechRecognizer(speech_config=config)
       speech_recognizer = speechsdk.SpeechRecognizer(speech_config=config,audio_config=audio_config)
       pronunciation_config.phoneme_alphabet = 'IPA'
       print("TEST2")
       pronunciation_config.apply_to(speech_recognizer)
       print("TEST3")
       result = speech_recognizer.recognize_once()
       print("TEST4")
       print(result.text)
       pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
       print(pronunciation_result.accuracy_score)
       print("TEST5")

   except Exception as ex:
       print("RECOGNIZE ERROR")
       print("Speech recognition failed: {}".format(ex))

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True)