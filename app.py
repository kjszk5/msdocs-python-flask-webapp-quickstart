from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session
import azure.cognitiveservices.speech as speechsdk
import os
import script_get

app = Flask(__name__)

app.config['SECRET_KEY'] = 'masterkey'

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/guide')
def guide():

   return render_template('guide.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/wav')
def wav():
   return render_template('wav.html')

@app.route('/script_view',methods=['GET'])
def script_view():
   page = int(request.args.get("page"))
   print(page)

   en_script,jp_script,page = script_get.script_get(request.args)
   session['en_script'] = en_script
   return render_template('script_view.html',page=page+1, en_script=en_script, jp_script=jp_script)



@app.route('/score',methods=['GET','POST'])
def score():
   page = int(session['page'])
   print(page)
   en_script = session['en_script']
   score = 0
   word_list = [0,0]
   pronunciation_text = ""

   print(en_script)
   if request.method == 'GET':
      print("GET")
#      print(request.form)
      print("GET END")
      audioFile = './static/wav/aaa'+str(page)+'.wav'
      COG_SERVICE_KEY="f475a189ffdd4362bfa09715ebc73660"
      COG_SERVICE_REGION="japaneast"
      config = speechsdk.SpeechConfig(subscription = COG_SERVICE_KEY,region = COG_SERVICE_REGION)
      reference_text = en_script
      audio_config = speechsdk.AudioConfig(filename=audioFile)
      pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=en_script,grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,enable_miscue=True)
      print("TEST1")
      try:
   #       speech_recognizer = speechsdk.SpeechRecognizer(speech_config=config)
         speech_recognizer = speechsdk.SpeechRecognizer(speech_config=config,audio_config=audio_config)
         pronunciation_config.phoneme_alphabet = 'IPA'
         print("TEST2")
         pronunciation_config.apply_to(speech_recognizer)
         print("TEST3")
         result = speech_recognizer.recognize_once()
         pronunciation_text = result.text
         print(pronunciation_text)
         print("TEST4")
         pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
         print("TEST5")
         score = [pronunciation_result.accuracy_score,pronunciation_result.fluency_score,pronunciation_result.completeness_score,pronunciation_result.pronunciation_score]
         #score = pronunciation_result.accuracy_score
         word_list = []
         for word in pronunciation_result.words:
            word_list.append([word.word,word.accuracy_score])
         print(score)
      except Exception as ex:
         print("RECOGNIZE ERROR")
         return render_template('recognize_error.html')
      print("TEST END")
   else:
      print("POST")
      data = request.data
      with open('./static/wav/aaa'+str(page)+'.wav','wb') as f:
         f.write(data)
      print("POST END")

#   name = request.form['key1']
   print(score)
#   os.remove('static/aaa.wav')

   return render_template('score.html',page=page+1,score=score,word_list=word_list,pronunciation_text=pronunciation_text)


@app.route('/review')
def review():

   return render_template('review.html')


if __name__ == '__main__':
   app.run(debug=True)