import customtkinter as ctk
from urllib.parse import urlparse, parse_qs
from io import BytesIO
import urllib.request
import sys
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
from pytube import YouTube

class Principal():
    def __init__(self, main=None):
        self.widget1 = Frame(main)
        self.widget1.pack()

        self.titulo = CTkLabel(main, text="Baixar Vídeos e Músicas do Youtube", fg_color="transparent")
        self.opcao_str = StringVar()
        self.opcao_label = CTkLabel(main, textvariable=self.opcao_str)
        global entrada_texto
        self.entrada_de_texto = CTkEntry(main, placeholder_text='Cole o link aqui')
        entrada_texto = self.entrada_de_texto
        self.botao_baixar = CTkButton(main, text='Ler Link', command=self.ler_link)
        self.variavel = StringVar(value="selecione")
        self.variavel.set('Selecione')
        self.combobox = CTkComboBox(main, values=["Vídeo", "Música"],
                                            command=self.opcao, variable=self.variavel)
        self.titulo.pack(padx=5,pady=5)
        self.entrada_de_texto.pack(padx=5,pady=5)
        self.combobox.pack(padx=5,pady=5)
        self.botao_baixar.pack(padx=5,pady=5)
        self.opcao_label.pack()
        self.ctg = 0
        
    def opcao(self,choice):
        self.opcao_str = self.opcao_str
        self.op = choice
        if self.op == 'Vídeo': 
            self.opcao_str.set('Você selecionou Vídeo')
        elif self.op == 'Música':
            self.opcao_str.set('Você selecionou Música')

    
    def ler_link(self, main=None):
        global video_id
        link = self.entrada_de_texto.get()
        video_id = self.extract_video_id(link)
        print(video_id)

        if self.op == 'Vídeo':
            if self.ctg == 0:
                self.musica_instance = Video(main)
                self.ctg =+ 1
            else:
                self.musica_instance.ocultar_widget2()
                self.musica_instance = Video(main)
        elif self.op == 'Música':
            if self.ctg == 0:
                self.musica_instance = Musica(main)
                self.ctg =+ 1
            else:
                self.musica_instance.ocultar_widget2()
                self.musica_instance = Musica(main)
                
    def extract_video_id(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        video_id = query.get('v')
        if video_id:
            return video_id[0]
        else:
            raise ValueError("URL Não é válida")
        

class Musica():
    def __init__(self, main=None):
        self.widget2 = CTkFrame(main)
        self.entrada_de_texto = None
        self.yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        self.titulo = self.yt.title
        self.thumbnail_yt = self.yt.thumbnail_url

        try:
            urllib.request.urlretrieve(self.thumbnail_yt, "thumbnail.jpg")
            print("Imagem salva! =)")
        except:
            erro = sys.exc_info()
            print("Ocorreu um erro:", erro)

        image = Image.open('thumbnail.jpg')
        new_image = image.resize((335, 190))
        new_image.save('thumbnail.jpg')
        self.imagem_nova = ImageTk.PhotoImage(new_image)

        self.imagem = CTkLabel(main, text='',image=self.imagem_nova)

        self.botao_baixar = CTkButton(main, text='Baixar Música', command=self.baixar)

        self.opcao_str = StringVar()
        self.opcao_label = CTkLabel(main, textvariable=self.opcao_str)
        self.opcao_str.set(self.titulo)

        self.opcao_label.pack()
        self.imagem.pack(padx=10,pady=10)
        self.botao_baixar.pack(padx=5,pady=5)

    def ocultar_widget2(self):
        self.widget2.pack_forget()
        self.botao_baixar.pack_forget()
        self.imagem.pack_forget()
        self.opcao_label.pack_forget()

    def baixar(self):
        audio = self.yt.streams.filter(only_audio=True)[0]
        audio.download()

class Video():
    def __init__(self, main=None):
        self.widget2 = CTkFrame(main)
        self.entrada_de_texto = None
        self.yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        self.titulo = self.yt.title
        self.thumbnail_yt = self.yt.thumbnail_url

        try:
            urllib.request.urlretrieve(self.thumbnail_yt, "thumbnail.jpg")
            print("Imagem salva! =)")
        except:
            erro = sys.exc_info()
            print("Ocorreu um erro:", erro)

        image = Image.open('thumbnail.jpg')
        new_image = image.resize((335, 190))
        new_image.save('thumbnail.jpg')
        self.imagem_nova = ImageTk.PhotoImage(new_image)

        self.imagem = CTkLabel(main, text='',image=self.imagem_nova)

        self.botao_baixar = CTkButton(main, text='Baixar Vídeo', command=self.baixar)

        self.opcao_str = StringVar()
        self.opcao_label = CTkLabel(main, textvariable=self.opcao_str)
        self.opcao_str.set(self.titulo)

        self.opcao_label.pack()
        self.imagem.pack(padx=10,pady=10)
        self.botao_baixar.pack(padx=5,pady=5)

    def ocultar_widget2(self):
        self.widget2.pack_forget()
        self.botao_baixar.pack_forget()
        self.imagem.pack_forget()
        self.opcao_label.pack_forget()

    def baixar(self):
        video = self.yt.streams.get_highest_resolution()
        video.download()

janela = CTk()
janela.geometry('560x510')
set_appearance_mode("dark")
set_default_color_theme("dark-blue")
janela.title('Download YT')
Principal(janela)

janela.mainloop()
