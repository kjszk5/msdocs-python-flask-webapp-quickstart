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

   print(en_script)
   if request.method == 'GET':
      print("GET")
#      print(request.form)
      print("GET END")
      audioFile = './static/aaa.wav'
      print("POST END")
      COG_SERVICE_KEY="f475a189ffdd4362bfa09715ebc73660"
      COG_SERVICE_REGION="japaneast"
      config = speechsdk.SpeechConfig(subscription = COG_SERVICE_KEY,region = COG_SERVICE_REGION)
      reference_text = en_script
      audio_config = speechsdk.AudioConfig(filename=audioFile)
      pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=en_script,grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,enable_miscue=True)
      print("TEST4")
      try:
   #       speech_recognizer = speechsdk.SpeechRecognizer(speech_config=config)
         speech_recognizer = speechsdk.SpeechRecognizer(speech_config=config,audio_config=audio_config)
         pronunciation_config.phoneme_alphabet = 'IPA'
         print("TEST2")
         pronunciation_config.apply_to(speech_recognizer)
         print("TEST3")
         result = speech_recognizer.recognize_once()
         print("TEST4")
         pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
         print("TEST5")
         score = [pronunciation_result.accuracy_score,pronunciation_result.fluency_score,pronunciation_result.completeness_score,pronunciation_result.pronunciation_score]
         #score = pronunciation_result.accuracy_score
         print(score)
      except Exception as ex:
         print("RECOGNIZE ERROR")
         return render_template('recognize_error.html')
      print("TEST END")
   else:
      print("POST")
      data = request.data
      with open('./static/aaa.wav','wb') as f:
         f.write(data)

#   name = request.form['key1']
   print(score)
   return render_template('score.html',page=page+1,score=score)

@app.route('/hello', methods=['GET','POST'])
def hello():
   name = request.form.get('name')
   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name, script = script, score = score)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True)