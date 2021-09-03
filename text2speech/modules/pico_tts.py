import subprocess

from text2speech.modules import TTS, TTSValidator


def lang_format(lang):
    if lang.startswith("de"):
        voice = "de-DE"
    elif lang.startswith("es"):
        voice = "es-ES"
    elif lang.startswith("fr"):
        voice = "fr-FR"
    elif lang.startswith("it"):
        voice = "it-IT"
    elif lang.startswith("en"):
        voice = "en-US"
        if "gb" in lang.lower() or "uk" in lang.lower():
            voice = "en-GB"
            return voice

class PicoTTS(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"lang": "en-US"}
        super(PicoTTS, self).__init__(config, PicoTTSValidator(self))
        self.voice = lang_format(self.lang)

    def get_tts(self, sentence, wav_file, lang=None):
        lang = lang or self.lang
        subprocess.call(
            ['pico2wave', '-l', lang_format(lang), "-w", wav_file, sentence])

        return wav_file, None

    def describe_voices(self):
        voices = {}
        for lang_code in ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR',
                          'it-IT']:
            voices[lang_code] = [lang_code]
        return voices


class PicoTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(PicoTTSValidator, self).__init__(tts)

    def validate_connection(self):
        try:
            subprocess.call(['pico2wave', '--help'])
        except:
            raise Exception(
                'PicoTTS is not installed. Run: '
                '\nsudo apt-get install libttspico0\n'
                'sudo apt-get install  libttspico-utils')

    def get_tts_class(self):
        return PicoTTS
