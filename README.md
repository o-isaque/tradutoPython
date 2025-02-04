**Documentação: Tradução Automática de Arquivos .po com LibreTranslate**

---

## **1. Introdução**

Esta documentação detalha o processo de configuração e utilização do **LibreTranslate** para traduzir automaticamente arquivos de localização no formato `.po`. O processo inclui a instalação do servidor de tradução, execução via Docker, e a utilização de um script Python para realizar a tradução em massa dos arquivos.

## **2. Requisitos**

Antes de iniciar, certifique-se de que possui os seguintes requisitos:

- **Windows 10/11**
- **Docker Desktop** instalado e configurado
- **Python 3.10+** instalado
- **Bibliotecas Python:** `requests` e `polib`

## **3. Instalação e Configuração**

### **3.1. Instalar Docker Desktop**

1. Baixe e instale o Docker Desktop a partir de [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
2. Durante a instalação, habilite o suporte ao **WSL 2**.
3. Verifique se a instalação foi concluída corretamente executando:
   ```bash
   docker --version
   ```

### **3.2. Iniciar o Servidor LibreTranslate**

1. Abra o **PowerShell** como administrador e execute o seguinte comando:
   ```bash
   docker run -d -p 5000:5000 libretranslate/libretranslate
   ```
2. Verifique se o servidor está rodando acessando [http://localhost:5000](http://localhost:5000) no navegador.
3. Teste a API com o seguinte comando:
   ```bash
   curl -X POST "http://localhost:5000/translate" -d "q=Hello World&source=en&target=pt"
   ```
   A resposta esperada deve ser:
   ```json
   {"translatedText":"Olá Mundo"}
   ```

## **4. Configuração do Ambiente Python**

### **4.1. Instalar Python e Bibliotecas Necessárias**

1. Baixe o Python em [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Durante a instalação, marque a opção **"Add Python to PATH"**.
3. Instale as bibliotecas necessárias executando:
   ```bash
   pip install requests polib
   ```

## \*\*5. Tradução de Arquivos \*\***`.po`**

### **5.1. Estrutura das Pastas**

Crie uma estrutura de pastas organizada:

```
traducoes/
  entrada/  # Coloque os arquivos .po aqui
  saida/    # Os arquivos traduzidos serão salvos aqui
```

### **5.2. Criar e Executar o Script Python**

Crie um arquivo `traduzir.py` com o seguinte código:

```python
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

```

### **5.3. Executar o Script**

Para rodar o script, utilize:

```bash
python traduzir.py
```

Os arquivos traduzidos serão salvos na pasta `traducoes/saida`.

## **6. Gerenciamento do Servidor LibreTranslate**

- **Parar o servidor:**
  ```bash
  docker stop $(docker ps -q --filter ancestor=libretranslate/libretranslate)
  ```
- **Reiniciar o servidor:**
  ```bash
  docker start $(docker ps -a -q --filter ancestor=libretranslate/libretranslate)
  ```
- **Remover o contêiner:**
  ```bash
  docker rm $(docker ps -a -q --filter ancestor=libretranslate/libretranslate)
  ```

## **7. Conclusão**

Seguindo estes passos, é possível automatizar a tradução de arquivos `.po` utilizando **LibreTranslate** e **Python**. O processo pode ser expandido para suportar mais idiomas e otimizado conforme a necessidade.

Se houver dúvidas ou problemas, verifique se o servidor do **LibreTranslate** está ativo e se as bibliotecas Python estão corretamente instaladas.

