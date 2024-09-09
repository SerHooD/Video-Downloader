import os
import yt_dlp
from PyQt5 import QtWidgets
from downloaderForm import Ui_Downloader
import sys

def get_desktop_path():
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:  # macOS ve Linux
        return os.path.join(os.path.expanduser('~'), 'Desktop')

desktop_path = get_desktop_path()

class  myApp(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(myApp,self).__init__()
        self.ui = Ui_Downloader()
        self.ui.setupUi(self)
        self.setWindowTitle("Video Downloader")

        self.ui.pushButton.clicked.connect(self.handleDownload)

    def handleDownload(self):
        self.ui.resultText.setText("Downloading.......")
        url = self.ui.url.text()
        self.videoDownload(url)
        self.ui.resultText.setText("Video downloaded successfully.")
        self.ui.url.setText("") 

    def update_progress(self, progress):
        self.ui.progressBar.setValue(progress)
        

    def videoDownload(self,url):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'verbose': True,
            'progress_hooks': [self.progress_hook],
                
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    
        except Exception as e:
            print(e)    
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            self.update_progress(int(percent))  # İlerleme çubuğunu güncelle





app= QtWidgets.QApplication(sys.argv)
win = myApp()
win.show()
sys.exit(app.exec_())




