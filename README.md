# Bot Voice Assistant

Este projeto é um assistente de voz desenvolvido em Python, capaz de converter fala em texto e vice-versa, utilizando modelos de reconhecimento de fala e síntese de voz.

## Funcionalidades

- Conversão de fala para texto.
- Conversão de texto para fala.
- Processamento de comandos de voz.

## Requisitos

- Python 3.8 ou superior.
- Bibliotecas listadas no arquivo `pyproject.toml`.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/ICE3BR/bot-voice-assistant.git
   cd bot-voice-assistant
   ```

2. Instale as dependências:
> Requisitos: Ter o Gerenciador de pacotes e projetos [UV](https://docs.astral.sh/uv/) 
   ```bash
   uv sync
   ```

## Uso

- Para iniciar o assistente de voz, execute:

  ```bash
  python listen_speak.py
  ```

- Para converter fala em texto, utilize:

  ```bash
  python speech_text.py
  ```

## Estrutura do Projeto

- `audios/`: Contém arquivos de áudio utilizados pelo assistente.
- `model-pt-small/`: Diretório para o modelo de reconhecimento de fala em português.
- `src/`: Código-fonte principal do assistente.
- `listen_speak.py`: Script para conversão de texto para fala.
- `speech_text.py`: Script para conversão de fala para texto.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais informações.

Para mais detalhes, visite o repositório no GitHub: [ICE3BR/bot-voice-assistant](https://github.com/ICE3BR/bot-voice-assistant)

