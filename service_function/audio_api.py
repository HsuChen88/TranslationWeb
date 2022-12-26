# 辨識音檔
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

def transcribe_audio(audio_path, language):
    r = sr.Recognizer()
    language = language_dict[language]
    
    try:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
        return r.recognize_google(audio, language=language)
    except ValueError:
        return "This type of file could not be transcribed"
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)
    return None
