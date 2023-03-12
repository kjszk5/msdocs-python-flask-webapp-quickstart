from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import azure.cognitiveservices.speech as speechsdk

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
   print('speech serviceのregionはこちらに設定しました:', config.region)
   reference_text="Hello World"
#   pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=reference_text,grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,enable_miscue=True)
   print("TEST2")
   try:
       recognizer = speechsdk.SpeechRecognizer(speech_config=config)
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