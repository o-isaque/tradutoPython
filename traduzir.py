import os
import requests
from polib import pofile

# Configurações
PASTA_ENTRADA = "C:/Users/Isaque/Documents/traducoes/entrada"
PASTA_SAIDA = "C:/Users/Isaque/Documents/traducoes/saida"
URL_LIBRETRANSLATE = "http://localhost:5000/translate"  # URL do servidor LibreTranslate

def traduzir_arquivo_po(arquivo_entrada, pasta_saida):
    # Carrega o arquivo .po
    po = pofile(arquivo_entrada)

    # Traduz as mensagens
    for entry in po:
        if entry.msgid and not entry.msgstr:  # Traduz apenas mensagens sem tradução
            payload = {
                "q": entry.msgid,
                "source": "en",  # Idioma de origem
                "target": "pt",  # Idioma de destino
                "format": "text"
            }
            response = requests.post(URL_LIBRETRANSLATE, data=payload)
            if response.ok:
                entry.msgstr = response.json()["translatedText"]
            else:
                print(f"Erro ao traduzir '{entry.msgid}': {response.status_code} - {response.text}")

    # Salva o arquivo traduzido na pasta de saída
    nome_arquivo = os.path.basename(arquivo_entrada)
    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
    po.save(caminho_saida)
    print(f"Tradução concluída: {caminho_saida}")

def main():
    # Cria a pasta de saída se não existir
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    # Processa cada arquivo .po na pasta de entrada
    for arquivo in os.listdir(PASTA_ENTRADA):
        if arquivo.endswith(".po"):
            caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)
            traduzir_arquivo_po(caminho_arquivo, PASTA_SAIDA)

if __name__ == "__main__":
    main()
