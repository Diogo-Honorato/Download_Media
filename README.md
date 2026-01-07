# 1. INTERFACE GRÁFICA

Os arquivos executáveis para a Interface Gráfica tanto para Linux quanto para Windows se encontram em [Releases](https://github.com/Diogo-Honorato/Download_Media/releases) apenas baixar e usar (plug-and-play).

# 2. Código Fonte
Caso queira fazer modificações ou seu próprio programa, será necessário baixar os Requisitos citados nos próximos capítulos.

## 2.1 REQUISITOS

Para que o código funcione, você precisa instalar os seguintes itens:

   -PYTHON:
   
      Certifique-se de ter o Python instalado em sua máquina.
   
      Download: www.python.org

   -BIBLIOTECA YT-DLP:
   
      Abra o seu terminal ou prompt de comando e instale a biblioteca via pip:
   
      > pip install -U yt-dlp

   -BIBLIOTECA CUSTOMTKINTER:
   
      Para a versão GUI, abra o seu terminal ou prompt de comando e instale a biblioteca via pip:
   
      > pip install customtkinter

 
   -FFMPEG (OBRIGATÓRIO):
   
      O script usa o FFmpeg para converter o áudio em MP3.
      
      - Windows: Baixe em ffmpeg.org ou via chocolatey: `choco install ffmpeg`
      
      - Linux: `sudo apt install ffmpeg`
      
      - Mac: `brew install ffmpeg`
   
      *Importante: O executável do FFmpeg deve estar no PATH do seu sistema.*

## 2.2 Como usar:
   O script funciona através do terminal seguindo a ordem:

   ```
   python3 download_media_CLI.py [MODO] [QUALIDADE] "LINK"
   ```
   obs.: Coloque aspas duplas no Link
   
   Para a versão de GUI:
   ```
   python3 download_media_GUI.py
   ```

### 2.2.1 Download de áudio (-a)
   Extrai apenas o áudio e converte para MP3.
   
   Se deixar em branco a qualidade irá para o modo padrão de 128 bits.

   QUALIDADES DE ÁUDIO DISPONÍVEIS (Bitrate):
   - 64  : Qualidade baixa (Economiza muito espaço)
   - 128 : Qualidade padrão (Recomendado)
   - 192 : Qualidade alta
   - 256 : Qualidade muito alta
   - 320 : Qualidade máxima (Arquivo maior)

   Exemplos:
   ```
   python3 download_media_CLI.py -a 128 "LINK_DO_VIDEO"
   ```

### 2.2.2 Download de vídeo (-v)

Baixa o vídeo completo em formato MP4.

Se deixar em branco a qualidade irá para o modo padrão 'max'.

   QUALIDADES DE VÍDEO DISPONÍVEIS (Resolução):
   - 360  : Qualidade baixa
   - 480  : Qualidade padrão (SD)
   - 720  : Alta definição (HD)
   - 1080 : Full High Definition (Full HD)
   - 1440 : Quad HD (2K)
   - 2160 : Ultra HD (4K)
   - max  : Baixa a maior resolução que o vídeo possuir

   Exemplos:
   ```
   python3 download_media_CLI.py -v 720 "LINK_DO_VIDEO"
   ```

# 3. REPOSITÓRIO E CUSTOMIZAÇÃO

- DOCUMENTAÇÃO OFICIAL:
  Para configurações avançadas (playlists, metadados, capas), 
  consulte o repositório da biblioteca yt-dlp:
  github.com

- ATUALIZAÇÃO:
  Se o YouTube ou qualquer site bloquear o download, atualize a ferramenta:
  pip install -U yt-dlp
