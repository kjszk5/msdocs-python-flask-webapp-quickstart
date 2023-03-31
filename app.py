from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,session, flash
from flask_login import current_user
import azure.cognitiveservices.speech as speechsdk
#from azure.identity import DefaultAzureCredential
#from azure.keyvault.secrets import SecretClient
import os
import script_get
import math

#KVUri  = "https://azure-speech-key.vault.azure.net/"

#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=KVUri, credential=credential)



app = Flask(__name__)

app.config['SECRET_KEY'] = 'masterkey'
app.config['USERNAME'] = 'TestUser'
app.config['PASSWORD'] = 'cwpanda'
app.config['PRACTICE_NO'] = 3

@app.route('/')
def index():
#   session['practice_count']=3
   session['question_num'] = 3
   practice_count = int(session['practice_count'])

   if 'first_access' not in session:
      session['first_access'] = True
      session['practice_count'] = 3
      practice_count = int(session['practice_count'])
   else:
      practice_count = session['practice_count']
   
   if session['flag']:
      session['practice_count'] = 999

   if "username" in session:
      username = session["username"]
      print("LoginOK")
      print(username)
   else:
      username = ""
      print("LoginNG")
   print('Request for index page received')
   return render_template('index.html',username=username,practice_count=practice_count)

#初めての方へ
@app.route('/new_user')
def new_user():

   return render_template('new_user.html')

#FAQ
@app.route('/faq')
def faq():

   return render_template('faq.html')

#ガイドライン
@app.route('/guideline')
def guideline():

   return render_template('guideline.html')


#お知らせ
@app.route('/information')
def information():

   return render_template('information.html')

#ご意見ご要望
@app.route('/consultation')
def consultation():

   return render_template('consultation.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/wav')
def wav():
   return render_template('wav.html')

@app.route('/login',methods=['GET'])
def login():
   print("LoginGET")
   return render_template('login.html') 

@app.route('/login',methods=['POST'])
def login_post():
   username = request.form["username"]
   password = request.form["password"]
   session["username"] = ""
   print("LOGIN POST")
   print(username)
   print(password)
   if username != app.config['USERNAME']:
      print('ユーザー名が異なります')
   elif password != app.config['PASSWORD']:
      print('パスワードが異なります')
   else:
      print("LoginOK!!")
      session["flag"] = True
      session["username"] = username
   return redirect(url_for('index'))


@app.route('/logout')
def logout():
   session.pop('username',None)
   session.pop('flag',None)
   session["username"] = ""
   session["flag"]=False
   username = ""
   session["practice_count"] = 3

#   return render_template('index.html',username=username)
   return redirect(url_for('index'))

#英文表示
@app.route('/script_view',methods=['GET'])
def script_view():
   question_no = int(request.args.get("question_no"))
   game_mode = 0
   session['game_mode'] = game_mode
   session['question_no'] = question_no
   print("SrciptView Start")
   print(request.method)
   print(question_no)
   practice_count = int(session['practice_count'])
   username = session['username']
   if practice_count == 0:
      print("PRACTICE END")
#      return render_template('index.html',username=username)
      return redirect(url_for('index'))

   practice_count = practice_count-1
   session['practice_count'] = practice_count

   if game_mode == 0:
      if question_no == 0:
         print("Script Get Start")
         en_script,jp_script,question_no = script_get.script_get()

      script_list = session['script_list']
      print(script_list)

      en_script = script_list[question_no][0]
      jp_script = script_list[question_no][1]
      print(en_script)
      print(jp_script)

      session['en_script'] = en_script
      return render_template('script_view.html',question_no=question_no, en_script=en_script, jp_script=jp_script)

   else:
      en_script = ""
      jp_script = ""
      return render_template('script_input.html',question_no=question_no,en_script=en_script, jp_script=jp_script)

#英文入力モード
@app.route('/script_input',methods=['GET'])
def script_input():
   question_no = int(request.args.get("question_no"))
   session['question_no'] = question_no
   game_mode = 1
   session['game_mode'] = game_mode

   en_script = ""
   jp_script = ""
   return render_template('script_input.html',question_no=question_no)

#英文表示(英文入力モード)
@app.route('/script_view2',methods=['GET','POST'])
def script_view2():
   print("Script View2")
   question_no = int(session['question_no'])

   en_script = request.form['input_script']
   jp_script = ""
   print(en_script)
   print(jp_script)
   if question_no == 0:
      script_list = [[en_script,jp_script,0,0,0,0]]
   else:
      script_list = session['script_list']
      script_list.append( [en_script,jp_script,0,0,0,0])
   session['script_list'] = script_list
   print(script_list)
   return render_template('script_view.html',question_no=question_no, en_script=en_script, jp_script=jp_script)


@app.route('/score',methods=['GET','POST'])
def score():
   print("Score Start")
   question_no = int(session['question_no'])
   game_mode = int(session['game_mode'])
   script_list = session['script_list']
   print(question_no)
   print(script_list)
   en_script = script_list[question_no][0]
   score = 0
   word_list = [0,0]
   pronunciation_text = ""
   question_num = int(session['question_num'])

   print(en_script)
   if request.method == 'GET':
      print("GET")
      audioFile = './static/wav/aaa'+str(question_no)+'.wav'
      COG_SERVICE_KEY="f475a189ffdd4362bfa09715ebc73660"
      COG_SERVICE_REGION="japaneast"
      config = speechsdk.SpeechConfig(subscription = COG_SERVICE_KEY,region = COG_SERVICE_REGION)
      reference_text = en_script
      audio_config = speechsdk.AudioConfig(filename=audioFile)
      pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=en_script,grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,enable_miscue=True)
      print("TEST1")
      try:
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
         print(pronunciation_result.accuracy_score)
         script_list[question_no][2] = pronunciation_result.accuracy_score
         script_list[question_no][3] = pronunciation_result.fluency_score
         script_list[question_no][4] = pronunciation_result.completeness_score
         script_list[question_no][5] = pronunciation_result.pronunciation_score
         print("TEST6")
         session['script_list'] = script_list
         print(script_list[question_no])
         print(script_list)
         #音節スコア、音素スコア集計
         word_list = []
         phoneme_list = []
         for word in pronunciation_result.words:
            word_list.append([word.word,word.accuracy_score])
            for phoneme in word.phonemes:
               phoneme_list.append([phoneme.phoneme,phoneme.accuracy_score,1])
         
         print(phoneme_list)
         #音素スコア平均計算
         for i in range(len(phoneme_list)):
            for j in range(i+1,len(phoneme_list)):
               if phoneme_list[i][0] == phoneme_list[j][0]:
                  phoneme_list[i][1] = (phoneme_list[i][1]*phoneme_list[i][2] + phoneme_list[j][1])/(phoneme_list[i][2] + phoneme_list[j][2])
                  phoneme_list[j][0] = 'ZZZ'
                  phoneme_list[i][2] = (phoneme_list[i][2] + phoneme_list[j][2])
         value_to_remove = 'ZZZ'
         phoneme_list_result = [row for row in phoneme_list if value_to_remove not in row]

         def compare(x):
            return x[1]
         phoneme_list_result.sort(key=compare,reverse=True)

         print("File Remove")
#         os.remove('./static/wav/aaa'+str(question_no)+'.wav')
         os.remove('./static/wav/aaa1.wav')


         print(phoneme_list_result)

      except Exception as ex:
         print("RECOGNIZE ERROR")
         print(question_no)
         return render_template('recognize_error.html',question_no = question_no)
      print("TEST END")
   else:
      print("POST")
      data = request.data
      with open('./static/wav/aaa'+str(question_no)+'.wav','wb') as f:
         f.write(data)
      print("POST END")

#   name = request.form['key1']
   print(score)
#   os.remove('static/aaa.wav')

   return render_template('score.html',question_no=question_no,game_mode=game_mode,score=script_list[question_no],word_list=word_list,pronunciation_text=pronunciation_text,question_num=question_num,phoneme_list_result=phoneme_list_result)

#振り返り
@app.route('/review')
def review():

   return render_template('review.html')

#全スコア確認
@app.route('/all_result')
def all_result():

   script_list = session['script_list']
   print("ALL_Result")
   print(script_list)
   total_score = [0,0,0]
   for col in range(len(script_list)):
      total_score[0] += script_list[col][2]
      total_score[1] += script_list[col][3]
      total_score[2] += script_list[col][4]
   
   average_score = [round(total_score[0]/len(script_list),1),round(total_score[1]/len(script_list),1),round(total_score[2]/len(script_list),1)]
   question_num = session['question_num']
   return render_template('all_result.html',script_list = script_list,average_score=average_score,question_num=question_num)

if __name__ == '__main__':
   app.run(debug=True)