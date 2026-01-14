
import speech_recognition as sr
import pyttsx3
import threading
import logging

class VoiceAgent:
    """
    [CODEX OS] Voice Command Center 🎙️
    Handles Speech-to-Text (STT) and Text-to-Speech (TTS).
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160) # Slightly faster speaking rate
        except:
            logging.warning("TTS Engine failed to initialize. Voice output disabled.")
            self.engine = None
            
        self.is_listening = False

    def speak(self, text):
        """Synthesizes text to speech."""
        if not self.engine: return
        
        def _speak_thread():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logging.error(f"TTS Error: {e}")
        
        threading.Thread(target=_speak_thread, daemon=True).start()

    def listen(self):
        """Listens for a command and returns text."""
        with sr.Microphone() as source:
            logging.info("Listening...")
            try:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio, language="pt-BR") # Default to PT-BR
                logging.info(f"Heard: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return "Desculpe, não entendi."
            except Exception as e:
                logging.error(f"STT Error: {e}")
                return None
