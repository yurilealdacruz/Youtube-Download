import customtkinter as ctk
from urllib.parse import urlparse, parse_qs
import sys
import yt_dlp as ytdlp
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
import webbrowser
import requests
from io import BytesIO

class Principal:
    def __init__(self, main=None):
        self.widget1 = Frame(main)
        self.widget1.pack()

        self.titulo = CTkLabel(main, text="Baixar Vídeos e Músicas do Youtube", fg_color="transparent")
        self.opcao_str = StringVar()
        self.opcao_label = CTkLabel(main, textvariable=self.opcao_str)
        self.entrada_de_texto = CTkEntry(main, placeholder_text='Cole o link aqui')
        self.botao_baixar = CTkButton(main, text='Ler Link', command=self.ler_link)
        self.variavel = StringVar(value="selecione")
        self.combobox = CTkComboBox(main, values=["Vídeo", "Música"], command=self.opcao, variable=self.variavel)
        self.info = CTkButton(main, text='Clique para mais informações', command=self.info)
        self.ctg = 0

        self.titulo.pack(padx=5, pady=5)
        self.entrada_de_texto.pack(padx=5, pady=5)
        self.combobox.pack(padx=5, pady=5)
        self.botao_baixar.pack(padx=5, pady=5)
        self.opcao_label.pack()
        self.info.pack(padx=5, pady=5)

    def info(self):
        webbrowser.open('https://github.com/yurilealdacruz/Youtube-Download')

    def opcao(self, choice):
        self.op = choice
        if self.op == 'Vídeo': 
            self.opcao_str.set('Você selecionou Vídeo')
        elif self.op == 'Música':
            self.opcao_str.set('Você selecionou Música')

    def ler_link(self):
        global video_id
        link = self.entrada_de_texto.get()
        try:
            video_id = self.extract_video_id(link)
            print(f"Video ID: {video_id}")
        except ValueError as e:
            print(f"Erro na URL: {e}")
            return

        if self.op == 'Vídeo':
            if self.ctg == 0:
                self.musica_instance = Video(self.widget1)
                self.ctg += 1
            else:
                self.musica_instance.ocultar_widget2()
                self.musica_instance = Video(self.widget1)
        elif self.op == 'Música':
            if self.ctg == 0:
                self.musica_instance = Musica(self.widget1)
                self.ctg += 1
            else:
                self.musica_instance.ocultar_widget2()
                self.musica_instance = Musica(self.widget1)
             
    def extract_video_id(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        video_id = query.get('v')
        if video_id:
            return video_id[0]
        else:
            raise ValueError("URL Não é válida")

class Musica:
    def __init__(self, main=None):
        self.widget2 = CTkFrame(main)
        self.yt_url = f"https://www.youtube.com/watch?v={video_id}"

        # Baixar e exibir a miniatura
        self.download_and_display_thumbnail(main)

        self.botao_baixar = CTkButton(main, text='Baixar Música', command=self.baixar)
        self.opcao_str = StringVar()
        self.opcao_label = CTkLabel(main, textvariable=self.opcao_str)
        self.opcao_str.set(self.get_title())

        self.opcao_label.pack()
        self.botao_baixar.pack(padx=5, pady=5)

    def download_and_display_thumbnail(self, main):
        ydl_opts = {'quiet': True, 'skip_download': True}
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.yt_url, download=False)
            thumbnail_url = info_dict.get("thumbnail", None)

        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url)
                image = Image.open(BytesIO(response.content))
                new_image = image.resize((335, 190))
                new_image.save('thumbnail.jpg')
                self.imagem_nova = ImageTk.PhotoImage(new_image)
                self.imagem = CTkLabel(main, text='', image=self.imagem_nova)
                self.imagem.pack(padx=10, pady=10)
                print("Imagem salva com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar a imagem: {e}")

    def get_title(self):
        ydl_opts = {'quiet': True, 'skip_download': True}
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.yt_url, download=False)
            return info_dict.get("title", "Título não encontrado")

    def ocultar_widget2(self):
        self.widget2.pack_forget()
        self.botao_baixar.pack_forget()
        self.imagem.pack_forget()
        self.opcao_label.pack_forget()

    def baixar(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{video_id} - musica.%(ext)s',
            'quiet': False,
        }
        try:
            with ytdlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.yt_url])
                print("Áudio baixado com sucesso!")
        except Exception as e:
            print(f"Erro ao baixar a música: {e}")

class Video:
    def __init__(self, main=None):
        self.widget2 = CTkFrame(main)
        self.yt_url = f"https://www.youtube.com/watch?v={video_id}"

        # Baixar e exibir a miniatura
        self.download_and_display_thumbnail(main)

        self.botao_baixar = CTkButton(main, text='Baixar Vídeo', command=self.baixar)
        self.opcao_str = StringVar()
        self.opcao_label = CTkLabel(main, textvariable=self.opcao_str)
        self.opcao_str.set(self.get_title())

        self.opcao_label.pack()
        self.botao_baixar.pack(padx=5, pady=5)

    def download_and_display_thumbnail(self, main):
        ydl_opts = {'quiet': True, 'skip_download': True}
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.yt_url, download=False)
            thumbnail_url = info_dict.get("thumbnail", None)

        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url)
                image = Image.open(BytesIO(response.content))
                new_image = image.resize((335, 190))
                new_image.save('thumbnail.jpg')
                self.imagem_nova = ImageTk.PhotoImage(new_image)
                self.imagem = CTkLabel(main, text='', image=self.imagem_nova)
                self.imagem.pack(padx=10, pady=10)
                print("Imagem salva com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar a imagem: {e}")

    def get_title(self):
        ydl_opts = {'quiet': True, 'skip_download': True}
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.yt_url, download=False)
            return info_dict.get("title", "Título não encontrado")

    def ocultar_widget2(self):
        self.widget2.pack_forget()
        self.botao_baixar.pack_forget()
        self.imagem.pack_forget()
        self.opcao_label.pack_forget()

    def baixar(self):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{video_id}-video.%(ext)s',
            'quiet': False,
        }
        try:
            with ytdlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.yt_url])
                print("Vídeo baixado com sucesso!")
        except Exception as e:
            print(f"Erro ao baixar o vídeo: {e}")

# Configuração da janela principal
janela = CTk()
janela.geometry('560x510')
set_appearance_mode("dark")
set_default_color_theme("dark-blue")
janela.title('Download YT')
Principal(janela)

janela.mainloop()

#pip install yt-dlp
#pip install customtkinter
#pip install pillow