import json
import os
import sys
import time

import pyaudio
from gtts import gTTS
from playsound import playsound
from vosk import KaldiRecognizer, Model

# Modo de depuração
DEBUG_MODE = False  # Altere para True para habilitar logs de depuração

# Caminho base do projeto
base_path = os.path.dirname(
    os.path.abspath(__file__)
)  # Obtém o diretório onde o script está localizado


class AssistenteVoz:
    def __init__(self):
        # Inicializa os caminhos, configurações e carrega o modelo
        self.model_path = os.path.join(
            base_path, "model-pt-small"
        )  # Caminho para o modelo
        self.audios_path = os.path.join(
            base_path, "audios"
        )  # Caminho para salvar os áudios
        self.rate = 16000  # Taxa de amostragem ajustada para 16kHz
        self.buffer_size = 4000  # Tamanho do buffer de áudio
        self.recognizer = None
        self.init_model()

    def init_model(self):
        # Verifica e carrega o modelo de reconhecimento de fala
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                "Modelo de linguagem PT-BR do Vosk não encontrado. Baixe em 'https://alphacephei.com/vosk/models' e extraia na pasta do projeto."
            )

        try:
            # Palavras específicas para reconhecimento e variações das palavras reconhecidas
            words = [
                "assistente",
                "navegador",
                "abrir navegador",
                "excel",
                "abrir excel",
                "powerpoint",
                "abrir powerpoint",
                "notas",
                "abrir notas",
                "edge",
                "abrir edge",
                "fechar",
            ]
            model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(model, self.rate, json.dumps(words))
            self.recognizer.SetWords(
                True
            )  # Ativa o detalhamento das palavras reconhecidas
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o modelo: {e}")

        # Cria a pasta de áudios, se não existir
        if not os.path.exists(self.audios_path):
            os.makedirs(self.audios_path)

    def cria_audio(self, audio, filename="tmp_audio.mp3"):
        """
        Converte texto em áudio e o reproduz.
        """
        audio_path = os.path.join(self.audios_path, filename)
        tts = gTTS(audio, lang="pt-br")  # Gera o áudio em português
        tts.save(audio_path)  # Salva o arquivo de áudio
        playsound(audio_path)  # Reproduz o áudio

    def ouvir_microfone(
        self, timeout=None, mensagem_espera="Aguardando a entrada de áudio..."
    ):
        """
        Escuta o áudio do microfone e retorna o texto reconhecido.
        """
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.buffer_size,
        )

        try:
            stream.start_stream()
            if mensagem_espera:
                print(mensagem_espera)  # Mensagem opcional enquanto escuta
            inicio = time.time()
            while True:
                data = stream.read(self.buffer_size, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    frase = eval(result).get("text", "").lower()  # Texto reconhecido
                    if DEBUG_MODE:
                        print("Debug - Texto reconhecido:", frase)
                    return frase

                if timeout and time.time() - inicio > timeout:
                    print("Tempo de escuta excedido.")
                    return None
        finally:
            # Garante que o fluxo será fechado
            stream.stop_stream()
            stream.close()
            p.terminate()

    def executar_comando(self, comando):
        """
        Executa um comando baseado no texto reconhecido.
        """
        comandos = {
            "navegador": lambda: os.system("start chrome.exe"),
            "abrir navegador": lambda: os.system("start chrome.exe"),
            "excel": lambda: os.system("start excel.exe"),
            "abrir excel": lambda: os.system("start excel.exe"),
            "powerpoint": lambda: os.system("start POWERPNT.exe"),
            "abrir powerpoint": lambda: os.system("start POWERPNT.exe"),
            "notas": lambda: os.system("notepad.exe"),
            "abrir notas": lambda: os.system("notepad.exe"),
            "edge": lambda: os.system("start msedge.exe"),
            "abrir edge": lambda: os.system("start msedge.exe"),
            "fechar": lambda: sys.exit(),
        }
        if comando in comandos:
            comandos[comando]()
            return True
        else:
            self.cria_audio("Comando não reconhecido.")
            return False


def main():
    assistente = AssistenteVoz()
    frase_ativacao = "assistente"  # Frase de ativação para iniciar o comando

    print("Iniciando assistente...")
    ultima_msg = time.time()

    while True:
        if time.time() - ultima_msg >= 10:
            print("Aguardando a frase de ativação...")
            ultima_msg = time.time()

        # Escuta a frase de ativação
        frase = assistente.ouvir_microfone(
            timeout=None, mensagem_espera="... ouvindo frase de ativação ..."
        )
        if frase and frase_ativacao in frase:
            print("Frase de ativação detectada!")
            print("Pronto para ouvir o comando. Fale agora!")

            som_ativacao = os.path.join(assistente.audios_path, "ativado.mp3")
            if os.path.exists(som_ativacao):
                playsound(som_ativacao)
            else:
                print("Arquivo de som 'ativado.mp3' não encontrado.")

            # Escuta o comando após a ativação
            comando = assistente.ouvir_microfone(
                timeout=8, mensagem_espera="... ouvindo comando ..."
            )
            if comando:
                print("Comando recebido:", comando)
                assistente.executar_comando(comando)
            else:
                print("Tempo esgotado. Voltando a aguardar a frase de ativação.")


if __name__ == "__main__":
    main()
