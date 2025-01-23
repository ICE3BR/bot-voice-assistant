import os
import sys

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# a API recognize_google não reconhece palavras com acentos ou caracteres especiais.


# Função responsável por criar o áudio
def cria_audio(audio):
    # Certifica-se de que o diretório existe
    if not os.path.exists("audios"):
        os.makedirs("audios")  # Cria a pasta se necessário

    # Caminho absoluto para evitar problemas de permissão
    audio_path = os.path.abspath("audios/hello.mp3")

    # Remove o arquivo existente, se necessário
    if os.path.exists(audio_path):
        os.remove(audio_path)

    tts = gTTS(audio, lang="pt-br")
    tts.save(audio_path)  # Salva o áudio
    print("Estou aprendendo o que você disse...")
    playsound(audio_path)  # Reproduz o áudio


# Função responsável por ouvir e reconhecer a fala
def ouvir_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=2)  # Reduz ruídos
        print("Diga alguma coisa:")
        audio = microfone.listen(source)  # Escuta o áudio do microfone

    try:
        frase = microfone.recognize_google(audio, language="pt-BR")  # Reconhece a fala
        if "navegador" in frase:
            os.system("start chrome.exe")
            return None
        elif "excel" in frase:
            os.system("start excel.exe")
            return None
        elif "powerPoint" in frase:
            os.system("start POWERPNT.exe")
            return None
        elif "edge" in frase:
            os.system("start msedge.exe")
            return None
        elif "notas" in frase:
            os.system("notepad.exe")
            return None
        elif "fechar" in frase:
            sys.exit()  # Encerra o programa
        print("Você disse: " + frase)
        return frase
    except sr.UnknownValueError:
        print("Não consegui entender o que foi dito.")
        return None


# Loop principal
while True:
    frase = ouvir_microfone()
    if frase:
        cria_audio(frase)
