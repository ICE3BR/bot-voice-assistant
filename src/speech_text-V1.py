import os
import sys
import time

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


# Função para criar áudio
def cria_audio(audio, filename="hello.mp3"):
    if not os.path.exists("audios"):
        os.makedirs("audios")
    audio_path = os.path.abspath(f"audios/{filename}")
    if os.path.exists(audio_path):
        os.remove(audio_path)
    tts = gTTS(audio, lang="pt-br")
    tts.save(audio_path)
    playsound(audio_path)


# Função para ouvir e reconhecer a fala
def ouvir_microfone(timeout=None, mensagem_espera="Aguardando a entrada de áudio..."):
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=2)
        if mensagem_espera:
            print(mensagem_espera)
        try:
            audio = microfone.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("Tempo de escuta excedido.")
            return None

    try:
        frase = microfone.recognize_google(audio, language="pt-BR")
        with open("audio_depuracao.wav", "wb") as f:
            f.write(audio.get_wav_data())  # Salva para depuração
        return frase.lower()  # Retorna a frase em letras minúsculas
    except sr.UnknownValueError:
        print("Não consegui entender o que foi dito.")
        return None


# Dicionário de comandos
def executar_comando(comando):
    comandos = {
        "navegador": lambda: os.system("start chrome.exe"),
        "excel": lambda: os.system("start excel.exe"),
        "teste": lambda: os.system("notepad.exe"),
        "powerpoint": lambda: os.system("start POWERPNT.exe"),
        "edge": lambda: os.system("start msedge.exe"),
        "fechar": lambda: sys.exit(),
    }
    if comando in comandos:
        comandos[comando]()
        return True
    else:
        cria_audio("Comando não reconhecido.")
        return False


# Função principal
def main():
    frase_ativacao = (
        "assistente"  # Frase de ativação (pode ser alterada para "alexa" ou outra)
    )
    cria_audio("IA ativado", "ativado.mp3")

    print("Iniciando assistente...")
    ultima_msg = time.time()

    while True:
        if time.time() - ultima_msg >= 10:
            print("Aguardando a frase de ativação...")
            ultima_msg = time.time()

        frase = ouvir_microfone(timeout=None, mensagem_espera=None)
        if frase and frase_ativacao in frase:
            print("Frase de ativação detectada!")
            playsound(
                "Python/Projetos/PLN/ativado.mp3"
            )  # Som de confirmação de ativação
            print("Pronto para ouvir o comando. Fale agora!")

            inicio = time.time()
            while time.time() - inicio < 5:
                comando = ouvir_microfone(timeout=5, mensagem_espera=None)
                if comando:
                    print("Comando recebido:", comando)
                    if executar_comando(comando):
                        break
            else:
                print("Tempo esgotado. Esperar a frase de ativação.")
                cria_audio("Tempo esgotado")


# Executa o programa
if __name__ == "__main__":
    main()
