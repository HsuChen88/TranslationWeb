# 辨識語音輸入內容
import speech_recognition as sr

language_dict = {
    "ar" : "ar-DZ",
    "ca" : "ca-ES",
    "zh-Hans" : "zh",
    "zh-Hant" : "zh-TW",
    "hr" : "hr-HR",
    "en" : "en-US",
    "fr" : "fr-FR",
    "de" : "de-DE",
    "el" : "el-GR",
    "he" : "iw-IL",
    "hi" : "hi-IN",
    "it" : "it-IT",
    "ja" : "ja-JP",
    "ko" : "ko-KR",
    "pt" : "pt-PT",
    "ru" : "ru-RU",
    "es" : "es-ES",
    "th" : "th-TH",
    "tr" : "tr-TR",
    "vi" : "vi-VN"
}

def transcribe_speaking(language):
    r = sr.Recognizer()
    language = language_dict[language]
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        recognized_text = r.recognize_google(audio, language=language)
        print('You said:', recognized_text)
        return recognized_text
    except sr.WaitTimeoutError:
        return "Please say something so that I can help you."
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)