# 1. REQUISITOS

Para que o código funcione, você precisa instalar os seguintes itens:

### 1.1 PYTHON:
   Certifique-se de ter o Python instalado em sua máquina.
   Download: www.python.org

### 1.2 BIBLIOTECA YT-DLP:
   Abra o seu terminal ou prompt de comando e instale a biblioteca via pip:
   > pip install -U yt-dlp

### 1.3 FFMPEG (OBRIGATÓRIO):
   O script usa o FFmpeg para converter o áudio em MP3.
   - Windows: Baixe em ffmpeg.org ou via chocolatey: `choco install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
   - Mac: `brew install ffmpeg`
   
   *Importante: O executável do FFmpeg deve estar no PATH do seu sistema.*

# 2. COMO USAR:
   O script funciona através do terminal seguindo a ordem:
   > python yt_download.py [MODO] [QUALIDADE] "LINK"

### 2.1 DOWNLOAD DE ÁUDIO (-a)
   Extrai apenas o áudio e converte para MP3.
   
   Se deixar em branco a qualidade irá para o modo padrão de 128 bits.

   QUALIDADES DE ÁUDIO DISPONÍVEIS (Bitrate):
   - 64  : Qualidade baixa (Economiza muito espaço)
   - 128 : Qualidade padrão (Recomendado)
   - 192 : Qualidade alta
   - 256 : Qualidade muito alta
   - 320 : Qualidade máxima (Arquivo maior)

   Exemplos:
   > python yt_download.py -a 128 "LINK_DO_VIDEO"

   > python yt_download.py -a 320 "LINK_DO_VIDEO"

### 2.2 DOWNLOAD DE VÍDEO (-v)

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
   > python yt_download.py -v 720 "LINK_DO_VIDEO"

   > python yt_download.py -v max "LINK_DO_VIDEO"


# 3. REPOSITÓRIO E CUSTOMIZAÇÃO


- MODIFICAÇÕES: 
  Para alterar o comportamento do script, edite o arquivo 
  "yt_download.py" conforme sua necessidade.

- DOCUMENTAÇÃO OFICIAL:
  Para configurações avançadas (playlists, metadados, capas), 
  consulte o repositório da biblioteca yt-dlp:
  github.com

- ATUALIZAÇÃO:
  Se o YouTube bloquear o download, atualize a ferramenta:
  pip install -U yt-dlp
