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


# Função para criar áudio
def cria_audio(audio, filename="tmp_audio.mp3"):
    """
    Cria um arquivo de áudio com a fala gerada a partir do texto fornecido.

    Parâmetros:
        audio (str): Texto a ser convertido em áudio.
        filename (str): Nome do arquivo de saída.
    """
    audios_path = os.path.join(base_path, "audios")  # Caminho para a pasta de áudios
    if not os.path.exists(audios_path):
        os.makedirs(audios_path)  # Cria a pasta de áudios se não existir
    audio_path = os.path.join(audios_path, filename)
    if os.path.exists(audio_path):
        os.remove(audio_path)  # Remove o arquivo anterior para evitar conflitos
    tts = gTTS(audio, lang="pt-br")  # Gera o áudio com texto em português
    tts.save(audio_path)  # Salva o áudio
    playsound(audio_path)  # Reproduz o áudio gerado


# Inicializa o modelo do Vosk
model_path = os.path.join(
    base_path, "model-pt-large"
)  # Caminho para o modelo PT-BR do Vosk
if not os.path.exists(model_path):
    print(
        "Modelo de linguagem PT-BR do Vosk não encontrado. Baixe em 'https://alphacephei.com/vosk/models' e extraia na pasta do projeto."
    )
    sys.exit(1)

try:
    # Define um vocabulário personalizado
    words = [
        "assistente",
        "navegador",
        "excel",
        "powerpoint",
        "notas",
        "edge",
        "fechar",
    ]
    model = Model(model_path)  # Carrega o modelo de reconhecimento de fala
    # rec = KaldiRecognizer(model, 48000)  # Sem vocabulário personalizado
    rec = KaldiRecognizer(
        model, 48000, json.dumps(words)
    )  # Inicializa o reconhecedor com o vocabulário personalizado
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    sys.exit(1)


# Função para ouvir e reconhecer a fala com Vosk
def ouvir_microfone_vosk(
    timeout=None, mensagem_espera="Aguardando a entrada de áudio..."
):
    """
    Escuta e reconhece a fala do usuário usando o modelo do Vosk.

    Parâmetros:
        timeout (int ou None): Tempo limite para escutar o áudio.
        mensagem_espera (str): Mensagem exibida enquanto escuta.

    Retorna:
        str: Texto reconhecido ou None se não entender nada.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=48000,
        input=True,
        frames_per_buffer=4000,
    )  # Configura o microfone com taxa de 48kHz e buffer padrão
    stream.start_stream()

    if mensagem_espera:
        print(mensagem_espera)  # Exibe a mensagem de espera
    inicio = time.time()
    while True:
        data = stream.read(
            4000, exception_on_overflow=False
        )  # Captura o áudio com buffer maior
        if rec.AcceptWaveform(data):
            result = rec.Result()
            frase = eval(result).get("text", "").lower()  # Extrai o texto reconhecido
            if DEBUG_MODE:
                print("Debug - Texto reconhecido:", frase)  # Log de depuração
            if frase:
                stream.stop_stream()
                stream.close()
                p.terminate()
                return frase

        if timeout and time.time() - inicio > timeout:
            print("Tempo de escuta excedido.")
            stream.stop_stream()
            stream.close()
            p.terminate()
            return None


# Dicionário de comandos
def executar_comando(comando):
    """
    Executa um comando baseado no texto reconhecido.

    Parâmetros:
        comando (str): Texto do comando reconhecido.

    Retorna:
        bool: True se o comando foi executado, False caso contrário.
    """
    comandos = {
        "navegador": lambda: os.system("start chrome.exe"),
        "excel": lambda: os.system("start excel.exe"),
        "notas": lambda: os.system("notepad.exe"),
        "powerpoint": lambda: os.system("start POWERPNT.exe"),
        "edge": lambda: os.system("start msedge.exe"),
        "fechar": lambda: sys.exit(),
    }
    if comando in comandos:
        comandos[comando]()  # Executa o comando correspondente
        return True
    else:
        cria_audio(
            "Comando não reconhecido."
        )  # Informa que o comando não foi reconhecido
        return False


# Função principal
def main():
    """
    Função principal que controla o fluxo do assistente virtual.
    """
    frase_ativacao = "assistente"  # Define a frase de ativação

    print("Iniciando assistente...")
    ultima_msg = time.time()

    while True:
        if time.time() - ultima_msg >= 10:
            print("Aguardando a frase de ativação...")
            ultima_msg = time.time()

        # Escuta a frase de ativação
        frase = ouvir_microfone_vosk(
            timeout=None, mensagem_espera="... ouvindo frase de ativação ..."
        )
        if frase and frase_ativacao in frase:
            print("Frase de ativação detectada!")
            print("Pronto para ouvir o comando. Fale agora!")

            # Inicia escuta do comando antes de reproduzir o som
            som_ativacao = os.path.join(base_path, "audios", "ativado.mp3")
            if os.path.exists(som_ativacao):
                playsound(som_ativacao)  # Reproduz som de ativação
            else:
                print("Arquivo de som 'ativado.mp3' não encontrado.")

            # Escuta um único comando
            comando = ouvir_microfone_vosk(
                timeout=8, mensagem_espera="... ouvindo comando ..."
            )
            if comando:
                print("Comando recebido:", comando)
                executar_comando(comando)
            else:
                print("Tempo esgotado. Voltando a aguardar a frase de ativação.")


# Executa o programa
if __name__ == "__main__":
    main()
