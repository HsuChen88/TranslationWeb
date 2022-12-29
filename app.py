from flask import Flask, render_template, request, url_for
import requests, uuid, json, os, re
from werkzeug.utils import secure_filename
from service_function.audio_api import *
from service_function.speak_api import *
from service_function.image_api import *
from service_function.pdf_vision_api import *
from copy import deepcopy
from pathlib import Path

web_url = 'https://aitranslation.azurewebsites.net'

UPLOAD_FOLDER = '.\\static'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

language_dict = {
    'ar' : 0,
    'ca' : 1,
    'zh-Hans' : 2,
    'zh-Hant' : 3,
    'hr' : 4,
    'en' : 5,
    'fr' : 6,
    'de' : 7,
    'el' : 8,
    'he' : 9,
    'hi' : 10,
    'it' : 11,
    'ja' : 12,
    'ko' : 13,
    'pt' : 14,
    'ru' : 15,
    'es' : 16,
    'th' : 17,
    'tr' : 18,
    'vi' : 19 
}

@app.route('/')
def index(title="即時翻譯"):
    return render_template('index.html', title=title)

def translate(input_text, language1, language2):
    key = "8af5f7c0e2f241e2bbe5717152675346"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    location = "eastus2"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': language1,
        'to': language2
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': input_text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated_text = response[0]['translations'][0]['text']
    return translated_text

@app.route('/text-translation', methods=['GET','POST'])
def text_translation(title='文字翻譯', input_text='', translated_text='', language1='', language2=''):
    selections_list = list('' for i in range(0,20))
    lang1_selected = deepcopy(selections_list)
    lang2_selected = deepcopy(selections_list)
    if request.method=='POST':
        input_text = request.values['input-text']
        language1 = request.values['language1']
        language2 = request.values['language2']
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        print("from ", language1, " to ", language2)
        translated_text = translate(input_text, language1, language2)
        return render_template('text-translation.html', title=title, input_text=input_text, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
    else:
        print("do nothing")
        print(request.args)
        language1 = 'en'
        language2 = 'zh-Hant'
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        return render_template('text-translation.html', title=title, input_text=input_text, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)

@app.route('/image-translation', methods=['GET','POST'])
def image_translation(title='圖片翻譯', translated_text='', language1='', language2=''):
    selections_list = list('' for i in range(0,20))
    lang1_selected = deepcopy(selections_list)
    lang2_selected = deepcopy(selections_list)
    if request.method=='POST':
        language1 = request.values['language1']
        language2 = request.values['language2']
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        if 'convert-url' in request.form:
            if request.form['input-url']:
                input_url = request.form['input-url']
                input_text = image_ocr(input_url)
                translated_text = translate(input_text, language1, language2)
                return render_template('image-translation.html', title=title, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
            else:
                return render_template('image-translation.html', title=title, translated_text="請輸入圖片網址或上傳圖片", language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)

        if 'convert-file' in request.form:
            image = request.files['input-image']
            if image:
                filename = image.filename
                print(type(filename), filename)
                print('endpoint', request.endpoint)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = web_url + url_for('static',filename=filename)
                print('image_url', image_url)
                input_text = image_ocr(read_image_url=image_url)
                translated_text = translate(input_text, language1, language2)
                lang1_selected[language_dict[language1]] =' selected'
                lang2_selected[language_dict[language2]] =' selected'
                # os.remove(app.config['UPLOAD_FOLDER']+'\\'+filename)  # permission error
                return render_template('image-translation.html', title=title, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
            else:
                return render_template('image-translation.html', title=title, translated_text="請輸入圖片網址或上傳圖片", language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
    else:
        print("do nothing")
        language1 = 'en'
        language2 = 'zh-Hant'
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'        
        return render_template('image-translation.html', title=title, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)

@app.route('/audio-translation', methods=['GET','POST'])
def audio_translation(title='語音翻譯', input_text='', translated_text='', language1='', language2=''):
    selections_list = list('' for i in range(0,20))
    lang1_selected = deepcopy(selections_list)
    lang2_selected = deepcopy(selections_list)
    
    if request.method=='POST':
        print(request.form)
        language1 = request.values['language1']
        language2 = request.values['language2']
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        if 'speak' in request.form:
            input_text = transcribe_speaking(language=language1)
            translated_text = translate(input_text, language1, language2)
            return render_template('audio-translation.html', title=title, input_text=input_text, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
        if 'convert' in request.form:
            file_type = request.files['input-audio'].content_type
            print("file_type", file_type)
            match = re.findall("^audio/", file_type)
            print('match', match)
            if match:   # 有音檔
                print("request.form", request.form)
                print("files", request.files)
                print("request.files['input-audio']", request.files['input-audio'])
                input_audio = request.files['input-audio']
                filename = input_audio.filename
                input_audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_path = app.config['UPLOAD_FOLDER']+'\\'+filename
                input_text = transcribe_audio(audio_path=file_path, language=language1)
                translated_text = translate(input_text, language1, language2)
                os.remove(app.config['UPLOAD_FOLDER']+'\\'+filename)
                return render_template('audio-translation.html', title=title, input_text=input_text, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
            else:
                print("no file")
                return render_template('audio-translation.html', title=title, input_text=input_text, translated_text="請放入音檔或開始說話", language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
        return render_template('audio-translation.html', title=title, input_text=input_text, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
    else:
        print("do nothing")
        language1 = 'en'
        language2 = 'zh-Hant'
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        return render_template('audio-translation.html', title=title, input_text=input_text, translated_text="請放入音檔或開始說話", language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)

@app.route('/file-translation', methods=['GET','POST'])
def file_translation(title='PDF文件翻譯', translated_text='', language1='', language2=''):
    selections_list = list('' for i in range(0,20))
    lang1_selected = deepcopy(selections_list)
    lang2_selected = deepcopy(selections_list)
    if request.method=='POST':
        language1 = request.values['language1']
        language2 = request.values['language2']
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        input_pdf = request.files['input-pdf']
        if input_pdf:
            filename = secure_filename(input_pdf.filename)
            input_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = app.config['UPLOAD_FOLDER']+'\\'+filename
            input_text = recognize_pdf(pdf_path=file_path)
            translated_text = translate(input_text, language1, language2)
            os.remove(app.config['UPLOAD_FOLDER']+'\\'+filename)
            return render_template('file-translation.html', title=title, input_text=input_text,translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)
        else:
            return render_template('file-translation.html', title=title, translated_text="請放入檔案", language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)

    else:
        print("do nothing")
        language1 = 'en'
        language2 = 'zh-Hant'
        lang1_selected[language_dict[language1]] =' selected'
        lang2_selected[language_dict[language2]] =' selected'
        return render_template('file-translation.html', title=title, translated_text=translated_text, language1=language1, language2=language2, lang1_selected=lang1_selected, lang2_selected=lang2_selected)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(port=5566, debug=True)

