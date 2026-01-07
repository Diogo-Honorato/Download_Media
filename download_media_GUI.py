import customtkinter as ctk
import yt_dlp
import sys
import os
import threading
from tkinter import filedialog
from tkinter import PhotoImage

# Configurações de Tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return ""

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

# Exceção personalizada para o cancelamento
class DownloadCancelled(Exception):
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # CONFIGURAÇÃO DA JANELA
        self.title("Download_Media")
        self.geometry("700x550")

        # ÍCONE
        try:
            
            caminho_icone = resource_path("icone.png")
            
            if os.path.exists(caminho_icone):
                self.img_icone = PhotoImage(file=caminho_icone)
                self.iconphoto(False, self.img_icone)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Configuração específica para Linux
        if sys.platform.startswith("linux"):
            self.attributes('-type', 'normal')



        self.configure(fg_color="#0f0f0f")
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        self.configure(fg_color="#0f0f0f")
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        # CONTEÚDO
        self.card = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15, border_width=1, border_color="#333")
        self.card.pack(padx=30, pady=30, fill="both", expand=True)

        # Entrada de URL
        self.url_entry = ctk.CTkEntry(self.card, height=45, placeholder_text="Cole o link aqui...",
                                      fg_color="#222", border_color="#444", corner_radius=10)
        self.url_entry.pack(pady=15, padx=30, fill="x")

        # Formatos (Horizontal)
        self.mode_var = ctk.StringVar(value="video")
        self.format_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.format_frame.pack(pady=10)

        ctk.CTkRadioButton(self.format_frame, text="Vídeo", variable=self.mode_var, 
                           value="video", command=self.atualizar_ui).pack(side="left", padx=20)
        ctk.CTkRadioButton(self.format_frame, text="Áudio", variable=self.mode_var, 
                           value="audio", command=self.atualizar_ui).pack(side="left", padx=20)

        # Frame para Qualidade e Extensão ficarem lado a lado
        self.options_row = ctk.CTkFrame(self.card, fg_color="transparent")
        self.options_row.pack(pady=10, padx=30, fill="x")

        # Coluna da Direita: Qualidade
        self.qual_col = ctk.CTkFrame(self.options_row, fg_color="transparent")
        self.qual_col.pack(side="right", expand=True)
        
        self.qual_label = ctk.CTkLabel(self.qual_col, text="RESOLUÇÃO MÁXIMA", font=("Inter", 10, "bold"), text_color="#D6D4D4")
        self.qual_label.pack()
        
        self.qualidades_video = ["Melhor Disponível", "2160", "1440", "1080", "720", "480"]
        self.combo_qualidade = ctk.CTkComboBox(self.qual_col, values=self.qualidades_video, 
                                               width=180, height=35, corner_radius=8, state="readonly") 
        self.combo_qualidade.pack(pady=5)
        self.combo_qualidade.set("1080")

        # Coluna da Esquerda: Extensão ["mp4", "mkv", "webm", "avi", "mov"]
        self.ext_col = ctk.CTkFrame(self.options_row, fg_color="transparent")
        self.ext_col.pack(side="left", expand=True)

        self.ext_label = ctk.CTkLabel(self.ext_col, text="FORMATO", font=("Inter", 10, "bold"), text_color="#D6D4D4")
        self.ext_label.pack()

        self.ext_var = ctk.StringVar(value="mp4")
        self.ext_var.trace_add("write", lambda *args: self.verificar_lossless())

        self.combo_extensao = ctk.CTkComboBox(self.ext_col, values=["mp4", "mkv", "webm", "avi", "mov"], 
                                               width=180, height=35, corner_radius=8, 
                                               state="readonly", variable=self.ext_var) 
        self.combo_extensao.pack(pady=5)


        # Seleção de Pasta
        self.path_btn = ctk.CTkButton(self.card, text=f"LOCAL DE SALVAMENTO", 
                                      fg_color="#0e456e", hover_color="#333", command=self.escolher_pasta)
        self.path_btn.pack(pady=20, padx=60, fill="x")
        
        self.path_display = ctk.CTkLabel(self.card, text=f"{self.download_path}", font=("Inter", 14), text_color="#D6D4D4")
        self.path_display.pack()

        
        self.progress_bar = ctk.CTkProgressBar(self.card, width=400, height=12, corner_radius=5)
 
        self.progress_bar.set(0)

        self.status_pct = ctk.CTkLabel(self.card, text="0%", font=("Inter", 10), text_color="#666")

        self.is_downloading = False
        self.stop_requested = False
        

        self.detalhes_erro = ctk.CTkTextbox(self.card, width=550, height=100, font=("Consolas", 13), fg_color="#0a0a0a", text_color="#888", border_width=1, border_color="#333")

        
        # Botão para expandir/recolher erro (inicia sem pack)
        self.btn_detalhes = ctk.CTkButton(self.card, text="▼ Mostrar Detalhes Técnicos", 
                                          width=150, height=20, font=("Inter", 13),
                                          fg_color="transparent", text_color="#888",
                                          hover_color="#222", command=self.toggle_detalhes)
        

        # Botão de Ação
        self.download_btn = ctk.CTkButton(self, text="START DOWNLOAD", font=("Inter", 14, "bold"),
                                          width=280, height=50, corner_radius=25,
                                          fg_color="#1f6aa5", hover_color="#144870",
                                          command=self.handle_button_click)
        self.download_btn.pack(pady=(0, 40))


    #Metodos
    def verificar_lossless(self):
        formato = self.ext_var.get()
        
        if formato in ["wav", "flac","ogg"]:

            self.combo_qualidade.configure(state="normal")
            
            self.combo_qualidade.set("Fidelidade Máxima")
            
            self.combo_qualidade.configure(state="disabled")
            self.qual_label.configure(text_color="#555")
        else:
            # Reativa o campo caso o usuário mude de volta para MP3 ou Vídeo
            self.combo_qualidade.configure(state="readonly")
            self.qual_label.configure(text_color="#D6D4D4")
            
            # Se o texto ainda for o de Lossless, volta para um padrão seguro
            if self.combo_qualidade.get() == "Fidelidade Máxima":
                if self.mode_var.get() == "audio":
                    self.combo_qualidade.set("128")
                else:
                    self.combo_qualidade.set("1080")

    def toggle_detalhes(self):
        if self.detalhes_erro.winfo_ismapped():
            self.detalhes_erro.pack_forget()
            self.btn_detalhes.configure(text="▼ Mostrar Detalhes Técnicos",font=("Inter", 13))
        else:
            self.detalhes_erro.pack(pady=10, padx=30, fill="x")
            self.btn_detalhes.configure(text="▲ Ocultar Detalhes Técnicos",font=("Inter", 13))
    
    def check_stop_hook(self, d):
        if self.stop_requested:
            raise Exception("DOWNLOAD_STOPPED_BY_USER")
   
    def handle_button_click(self):
        if not self.is_downloading:
            self.start_download_thread()
        else:
            # Se já estiver baixando, sinalizamos a parada
            self.stop_requested = True
            self.download_btn.configure(text="PARANDO...", state="disabled")
            self.status_pct.configure(text="Solicitando cancelamento...", text_color="orange")

    def stop_download(self):
        self.stop_requested = True
        self.status_pct.configure(text="Cancelando...", text_color="red",font=("Inter", 12, "bold"))
        self.download_btn.configure(state="disabled")

    def progress_hook(self, d):
        if self.stop_requested:
            raise DownloadCancelled("Usuário cancelou o download")
            
        if d['status'] == 'downloading':
           
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            baixado = d.get('downloaded_bytes', 0)

            if total:
                porcentagem = baixado * 100 / total
                
                self.progress_bar.set(porcentagem / 100)
                
                self.status_pct.configure(
                    text=f"Baixando: {porcentagem:.1f}%", 
                    text_color="#1f6aa5",
                    font=("Inter", 12, "bold")
                )
            else:

                self.status_pct.configure(text="Baixando... (Tamanho desconhecido)", text_color="#1f6aa5",font=("Inter", 12, "bold"))

        if d['status'] == 'finished':
            self.progress_bar.set(1.0)
            self.status_pct.configure(text="Download concluído! Processando...", text_color="#00FF00",font=("Inter", 12, "bold"))

    def escolher_pasta(self):
        diretorio = filedialog.askdirectory()
        if diretorio:
            self.download_path = diretorio
            self.path_display.configure(text=f"{diretorio}")

    def atualizar_ui(self):
        if self.mode_var.get() == "video":
            self.qual_label.configure(text="RESOLUÇÃO MÁXIMA")
            self.combo_qualidade.configure(values=self.qualidades_video)
            self.combo_qualidade.set("1080")
            
            # Lista estendida de vídeo
            formatos_video = ["mp4", "mkv", "webm", "avi", "mov"]
            self.combo_extensao.configure(values=formatos_video)
            self.combo_extensao.set("mp4")
            
        else:
            self.qual_label.configure(text="BITRATE (KBPS)")
            self.combo_qualidade.configure(values=["320", "256", "192", "128"])
            self.combo_qualidade.set("128")
            
            # Lista estendida de áudio
            formatos_audio = ["mp3", "m4a", "wav", "flac", "ogg"]
            self.combo_extensao.configure(values=formatos_audio)
            self.combo_extensao.set("mp3")

    def start_download_thread(self):
        self.download_btn.configure(state="disabled", text="BAIXANDO...")
        threading.Thread(target=self.download_logic, daemon=True).start()

    def download_logic(self):
        url = self.url_entry.get().strip()
        quality_raw = self.combo_qualidade.get()

        self.btn_detalhes.pack_forget()
        self.detalhes_erro.pack_forget()
        self.detalhes_erro.delete("0.0", "end") # Limpa o texto antigo

        # Se for o texto informativo ou melhor disponível, define como max
        if quality_raw in ["Melhor Disponível", "Fidelidade Máxima"]:
            quality = "max"
        else:
            quality = quality_raw

        # Se a URL estiver vazia
        if not url or url == "":
            self.progress_bar.pack(pady=(20, 0)) 
            self.status_pct.pack(pady=(5, 10))
            self.status_pct.configure(text="Erro: URL Vazia", text_color="red", font=("Inter", 12, "bold"))
            self.progress_bar.set(0)
            self.download_btn.configure(state="normal", text="START DOWNLOAD")

            def esconder_erro():
                self.progress_bar.pack_forget()
                self.status_pct.pack_forget()
            self.after(3000, esconder_erro)
            return

        # Limpa detalhes de erros anteriores antes de começar
        self.detalhes_erro.pack_forget()
        
        self.progress_bar.pack(pady=(20, 0)) 
        self.status_pct.pack(pady=(5, 10))

        self.is_downloading = True
        self.stop_requested = False
        self.download_btn.configure(text="STOP DOWNLOAD", fg_color="#cc0000", hover_color="#990000")
        self.progress_bar.set(0)
        self.status_pct.configure(text="Iniciando...", text_color="#D6D4D4", font=("Inter", 12, "bold"))

        mode = self.mode_var.get()
        extension = self.ext_var.get() # Pega a extensão escolhida (mp4, mkv, mp3, etc)

        quality_raw = self.combo_qualidade.get()
        quality = "max" if quality_raw == "Melhor Disponível" else quality_raw
        ffmpeg_dir = get_ffmpeg_path()

        ydl_opts = {
            'restrictfilenames': True,
            'outtmpl': f'{self.download_path}/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_dir if ffmpeg_dir != "" else None,
            'nocheckcertificate': True,
            'quiet': True,
            'progress_hooks': [self.progress_hook, self.check_stop_hook],
            'impersonate_client': 'android-music',
            'source_address': '0.0.0.0',
            'extractor_args': {'youtube': {'player_client': ['web_safari']}},
        }

        if mode == 'audio':

            codec = 'vorbis' if extension == 'ogg' else extension

            post_opts = {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': codec , # mp3, wav, flac, etc.
            }
            
            # SÓ adicionamos a qualidade (bitrate) se NÃO for um formato sem perdas
            # Formatos lossless (WAV/FLAC) ignoram esse parâmetro
            if extension not in ["wav", "flac","ogg"]:
                post_opts['preferredquality'] = quality
            
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [post_opts],
            })

            if extension == 'ogg':
                ydl_opts['outtmpl'] = f'{self.download_path}/%(title)s.ogg'

        else:
            # Configuração de Vídeo
            format_str = f'bestvideo[height<={quality}]+bestaudio/best/best' if quality.isdigit() else 'bestvideo+bestaudio/best'
            ydl_opts.update({
                'format': format_str,
                'merge_output_format': extension, # Define o container (mp4, mkv, avi)
            })
            
            # Garante que o FFmpeg converta para o formato final escolhido
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': extension,
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not self.stop_requested:
                self.status_pct.configure(text="Concluído com Sucesso!", text_color="#00FF00", font=("Inter", 12, "bold"))
                self.progress_bar.set(1.0)
            
        except DownloadCancelled:
            self.status_pct.configure(text="Download Interrompido", text_color="#FF9900", font=("Inter", 12, "bold"))
            self.progress_bar.set(0)
        
        except Exception as e:
            self.status_pct.configure(text="Erro no Processo", text_color="red", font=("Inter", 12, "bold"))
            
            self.btn_detalhes.pack(pady=5)
            
            self.detalhes_erro.delete("0.0", "end")
            self.detalhes_erro.insert("0.0", f"DETALHES TÉCNICOS:\n{str(e)}")
            self.progress_bar.set(0)

        # FINALIZAÇÃO
        self.is_downloading = False
        self.stop_requested = False
        self.download_btn.configure(
            text="START DOWNLOAD", 
            fg_color="#1f6aa5", 
            hover_color="#144870", 
            state="normal"
        )
      


if __name__ == "__main__":
    app = App()
    app.mainloop()
