import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Button, Label, Entry, Style
from downloader.downloader import VideoDownloader
from utils.config import ConfigManager
from utils.progress import ProgressManager

class VideoDownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Downloader de Vídeos")
        self.root.geometry("500x250")

        self.config_manager = ConfigManager()
        self.video_downloader = VideoDownloader(self.update_progress, self.download_complete)
        self.progress_manager = ProgressManager()

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = Style()
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TEntry', font=('Helvetica', 10))

    def create_widgets(self):
        self.url_label = Label(self.root, text="URL do Vídeo:")
        self.url_label.pack(pady=5)

        self.url_entry = Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        self.destination_var = tk.StringVar(value=self.config_manager.load_config())
        self.destination_label = Label(self.root, text="Pasta de Destino:")
        self.destination_label.pack(pady=5)

        self.destination_entry = Entry(self.root, textvariable=self.destination_var, width=50)
        self.destination_entry.pack(pady=5)

        self.destination_button = Button(self.root, text="Escolher Pasta", command=self.choose_directory)
        self.destination_button.pack(pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, fill=tk.X, padx=20)

        self.download_button = Button(self.root, text="Baixar", command=self.start_download)
        self.download_button.pack(pady=10)

        self.stop_button = Button(self.root, text="Parar", command=self.stop_download)
        self.stop_button.pack(pady=5)

    def choose_directory(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination_var.set(folder_selected)

    def start_download(self):
        url = self.url_entry.get()
        destination = self.destination_var.get()
        if not url or not destination:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos.")
            return

        self.config_manager.save_config(destination)
        self.video_downloader.start_download(url, destination)

    def stop_download(self):
        self.video_downloader.stop_download()

    def update_progress(self, progress):
        self.progress_var.set(progress)

    def download_complete(self, success, message):
        if success:
            messagebox.showinfo("Download Completo", "O download foi concluído com sucesso!")
        else:
            messagebox.showerror("Erro de Download", message)

    def run(self):
        self.root.mainloop()
