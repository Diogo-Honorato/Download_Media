import yt_dlp 
import sys
import os

def download_content(video_url, path, mode, quality):
    if not os.path.exists(path):
        os.makedirs(path)

    ydl_opts = {
        'restrictfilenames': True,
        'outtmpl': f'{path}/%(title)s.%(ext)s',
    }

    if mode == 'audio':
        print(f"\n[Modo Áudio | Qualidade: {quality}kbps]\n\n")
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
        })
    else:
        
        if quality in ['0', 'max', 'best']:
            format_str = 'bestvideo+bestaudio/best'
            print(f"\n[Modo Vídeo | Melhor Resolução disponível]\n")
        else:
            
            format_str = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best'
            print(f"\n[Modo Vídeo | Limite de Resolução: {quality}p]\n")
        
        ydl_opts.update({
            'format': format_str,
            'merge_output_format': 'mp4',
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            print(f"\n[DOWNLOAD {mode.upper()} COMPLETED]\n")
        except Exception as e:
            print(f"\n[ERROR DOWNLOADING CONTENT: {e}]\n")

def main():

    if len(sys.argv) >= 4:
        mode_input = sys.argv[1].lower()
        qualidade = sys.argv[2]
        link = sys.argv[3]

        if mode_input in ['-a', 'audio']:
            download_content(link, "download", "audio", qualidade)
        elif mode_input in ['-v', 'video']:
            download_content(link, "download", "video", qualidade)
        else:
            print("\nMODO INVÁLIDO!")
    
    elif len(sys.argv) == 3:
        mode_input = sys.argv[1].lower()
        link = sys.argv[2]
        padrao = "128" if mode_input in ['-a', 'audio'] else "max"
        print(f"\n[Qualidade não informada, usando padrão: {padrao}]\n")
        download_content(link, "download", "audio" if mode_input in ['-a', 'audio'] else "video", padrao)
            
    else:
        print('\nCOMO USAR(Para mais informçoes de configuraçao de qualidade consulte o README.txt):')
        print('Áudio: python3 yt_down.py -a <QUALIDADE> "URL"')
        print('Vídeo (1080p): python3 yt_down.py -v <QUALIDADE> "URL"')

if __name__ == "__main__":
    main()
