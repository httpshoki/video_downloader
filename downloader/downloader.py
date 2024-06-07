import threading
import yt_dlp

class VideoDownloader:
    def __init__(self, progress_callback, completion_callback):
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
        self.download_thread = None
        self.stop_event = threading.Event()

    def start_download(self, url, destination):
        self.stop_event.clear()
        self.download_thread = threading.Thread(target=self._download_video, args=(url, destination))
        self.download_thread.start()

    def stop_download(self):
        self.stop_event.set()
        if self.download_thread:
            self.download_thread.join()

    def _download_video(self, url, destination):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{destination}/%(title)s.%(ext)s',
            'progress_hooks': [self._progress_hook]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                self.completion_callback(True, "O download foi concluído com sucesso!")
            except Exception as e:
                if self.stop_event.is_set():
                    self.completion_callback(False, "O download foi cancelado.")
                else:
                    self.completion_callback(False, str(e))

    def _progress_hook(self, d):
        if self.stop_event.is_set():
            raise Exception("Download interrompido pelo usuário.")
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes:
                progress = downloaded_bytes / total_bytes * 100
                self.progress_callback(progress)
