import sys
from custome_errors import *
sys.excepthook = my_excepthook
import os
import pyperclip
import vlc
import gui
import guiTools
from webbrowser import open as openLink
import language,settings_handler
import app
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
import os
try:
    os.add_dll_directory(os.path.join(settings_handler.get("g","path")))
except:
    os.add_dll_directory(os.path.join(os.getcwd()))

class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        self.path="None"
        self.type="None"
        self.folder_play=False
        self.folder_files=[]
        self.folder_path=""
        self.folder_index=0
        layout=qt.QVBoxLayout()
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.video_widget = qt.QFrame()
        self.player.toggle_fullscreen()
        self.player.set_hwnd(self.video_widget.winId())
        self.video_widget.setGeometry(500,500,500,500)
        layout.addWidget(self.video_widget)
        if len(sys.argv) > 1:
            media = self.instance.media_new(" ".join(sys.argv[1::]))
            self.player.set_media(media)
            self.player.play()
        else:
            settings_handler.set("g","path",os.getcwd())
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        mb=self.menuBar()
        open=mb.addMenu(_("open"))
        file=qt1.QAction(_("open file"),self)
        open.addAction(file)
        file.triggered.connect(self.oopen)
        file.setShortcut("ctrl+o")
        folder=qt1.QAction(_("open folder"),self)
        open.addAction(folder)
        folder.triggered.connect(self.ofolder)
        folder.setShortcut("shift+o")
        url=qt1.QAction(_("open link from internet"),self)
        open.addAction(url)
        url.triggered.connect(self.ourl)
        url.setShortcut("ctrl+shift+o")
        player=mb.addMenu(_("player"))
        play=qt1.QAction(_("play"),self)
        player.addAction(play)
        play.triggered.connect(self.oplay)
        play.setShortcut("space")
        re=qt1.QAction(_("rewind"),self)
        player.addAction(re)
        re.triggered.connect(lambda:self.player.set_time(self.player.get_time() - 10000))
        re.setShortcut("alt+left")
        fast=qt1.QAction(_("fast forward"),self)
        player.addAction(fast)
        fast.triggered.connect(lambda:self.player.set_time(self.player.get_time() + 10000))
        fast.setShortcut("alt+right")
        stop=qt1.QAction(_("stop"),self)
        player.addAction(stop)
        stop.triggered.connect(self.ostop)
        stop.setShortcut("ctrl+space")
        fastest=player.addMenu(_("speed"))
        fastr=qt1.QAction(_("increase"),self)
        fastest.addAction(fastr)
        fastr.triggered.connect(lambda:self.ofast("+"))
        fastr.setShortcut("f")
        fastd=qt1.QAction(_("decrease"),self)
        fastest.addAction(fastd)
        fastd.triggered.connect(lambda:self.ofast("-"))
        fastd.setShortcut("shift+f")
        nor=qt1.QAction(_("normal"),self)
        fastest.addAction(nor)
        nor.triggered.connect(lambda:self.ofast("n"))
        nor.setShortcut("ctrl+f")
        volume=player.addMenu(_("volume"))
        vu=qt1.QAction(_("increase"),self)
        volume.addAction(vu)
        vu.triggered.connect(lambda:self.player.audio_set_volume(self.player.audio_get_volume() + 10))
        vu.setShortcut("alt+up")
        vd=qt1.QAction(_("decrease"),self)
        volume.addAction(vd)
        vd.triggered.connect(lambda:self.player.audio_set_volume(self.player.audio_get_volume() - 10))
        vd.setShortcut("alt+down")
        vn=qt1.QAction(_("normal"),self)
        volume.addAction(vn)
        vn.triggered.connect(lambda:self.player.audio_set_volume(100))
        self.vm=qt1.QAction(_("mute"),self)
        volume.addAction(self.vm)
        self.vm.triggered.connect(self.omute)
        self.muted=False
        self.vm.setShortcut("m")
        goTo=player.addMenu(_("go to"))
        p10=qt1.QAction(_("10%"),self)
        goTo.addAction(p10)
        p10.triggered.connect(lambda:self.player.set_time(10*self.player.get_length()//100))
        p10.setShortcut("1")
        p20=qt1.QAction(_("20%"),self)
        goTo.addAction(p20)
        p20.triggered.connect(lambda:self.player.set_time(20*self.player.get_length()//100))
        p20.setShortcut("2")
        p30=qt1.QAction(_("30%"),self)
        goTo.addAction(p30)
        p30.triggered.connect(lambda:self.player.set_time(30*self.player.get_length()//100))
        p30.setShortcut("3")
        p40=qt1.QAction(_("40%"),self)
        goTo.addAction(p40)
        p40.triggered.connect(lambda:self.player.set_time(40*self.player.get_length()//100))
        p40.setShortcut("4")
        p50=qt1.QAction(_("50%"),self)
        goTo.addAction(p50)
        p50.triggered.connect(lambda:self.player.set_time(50*self.player.get_length()//100))
        p50.setShortcut("5")
        p60=qt1.QAction(_("60%"),self)
        goTo.addAction(p60)
        p60.triggered.connect(lambda:self.player.set_time(60*self.player.get_length()//100))
        p60.setShortcut("6")
        p70=qt1.QAction(_("70%"),self)
        goTo.addAction(p70)
        p70.triggered.connect(lambda:self.player.set_time(70*self.player.get_length()//100))
        p70.setShortcut("7")
        p80=qt1.QAction(_("80%"),self)
        goTo.addAction(p80)
        p80.triggered.connect(lambda:self.player.set_time(80*self.player.get_length()//100))
        p80.setShortcut("8")
        p90=qt1.QAction(_("90%"),self)
        goTo.addAction(p90)
        p90.triggered.connect(lambda:self.player.set_time(90*self.player.get_length()//100))
        p90.setShortcut("9")
        p0=qt1.QAction(_("replay"),self)
        goTo.addAction(p0)
        p0.triggered.connect(lambda:self.player.set_time(0))
        p0.setShortcut("0")
        jump=qt1.QAction(_("jump to time"),self)
        goTo.addAction(jump)
        jump.triggered.connect(lambda:gui.JumpToTime(self,self.getdu(self.player.get_length())).exec())
        jump.setShortcut("ctrl+j")
        bast=qt1.QAction(_("paste file or link"),self)
        open.addAction(bast)
        bast.triggered.connect(self.onpaste)
        bast.setShortcut("ctrl+v")
        copy=qt1.QAction(_("copy file path"),self)
        player.addAction(copy)
        copy.triggered.connect(lambda:pyperclip.copy(self.path))
        copy.setShortcut("ctrl+c")
        info=qt1.QAction(_("file info"),self)
        player.addAction(info)
        info.triggered.connect(self.oninfo)
        info.setShortcut("i")
        self.MF=mb.addMenu(_("folder"))
        self.MF.setDisabled(True)
        nextf=qt1.QAction(_("next file"),self)
        nextf.triggered.connect(lambda: self.control(0))
        nextf.setShortcut("tab")
        self.MF.addAction(nextf)
        bref=qt1.QAction(_("previous"),self)
        bref.triggered.connect(lambda: self.control(1))
        bref.setShortcut("shift+tab")
        self.MF.addAction(bref)
        firstf=qt1.QAction(_("go to first file"),self)
        firstf.triggered.connect(lambda: self.control(2))
        firstf.setShortcut("home")
        self.MF.addAction(firstf)
        lastf=qt1.QAction(_("go to last file"),self)
        lastf.triggered.connect(lambda: self.control(3))
        lastf.setShortcut("end")
        self.MF.addAction(lastf)
        gototime=qt1.QAction(_("go to  file"),self)
        gototime.triggered.connect(lambda:gui.GoToFile(self).exec())
        gototime.setShortcut("ctrl+g")
        self.MF.addAction(gototime)
        tools=mb.addMenu(_("tools"))
        tts=qt1.QAction(_("text to speech"),self)
        tools.addAction(tts)
        tts.triggered.connect(lambda:gui.TextToSpeech(self).exec())
        help=mb.addMenu(_("help"))
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:openLink("https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:openLink("https://t.me/tprogrammers"))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:openLink("https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
    def oopen(self):
        file=qt.QFileDialog(self)
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptOpen)
        if file.exec() == qt.QFileDialog.DialogCode.Accepted:
            media = self.instance.media_new(file.selectedFiles()[0])
            self.player.set_media(media)
            self.player.play()
            self.path=file.selectedFiles()[0]
            self.type="file"
            self.MF.setDisabled(True)
    def oplay(self):
        if self.player.get_state()!=vlc.State.Ended:
            if self.player.is_playing():
                self.player.pause()
            else:
                self.player.play()
        else:
            media = self.instance.media_new(self.path)
            self.player.set_media(media)
            self.player.play()
    def ourl(self):
        text,ok=qt.QInputDialog.getText(self,_("url"),_("type the link "))
        if ok:
            media = self.instance.media_new(text)
            self.player.set_media(media)
            self.player.play()
            self.path=text
            self.type="link"
            self.MF.setDisabled(True)
    def ofast(self,a):
        state=self.player.get_rate()
        if state==0.1:
            pass
        elif state==2.0:
            pass
        else:
            if a=="-":
                self.player.set_rate(state - 0.1)
            elif a=="+":
                self.player.set_rate(state + 0.1)
            else:
                self.player.set_rate(1.0)
    def omute(self):
        if self.muted:
            self.vm.setText(_("mute"))
            self.player.audio_set_volume(100)
            self.muted=False
        else:
            self.vm.setText(_("un mute"))
            self.player.audio_set_volume(00)
            self.muted=True
    def getdu(self,duration):
        u=duration//3600000
        m1=duration%3600000
        m=m1//60000
        s1=duration%60000
        if m == 0 and u==0:
            s = duration // 1000
        else:
            s=s1//1000
        return u,m,s
    def onpaste(self):
        text=pyperclip.paste()  
        if os.path.isdir(text):
            self.getFiles(text)
            if len(self.folder_files)>0:
                self.playMedia(os.path.join(self.folder_path,self.folder_files[0]))
                self.MF.setDisabled(False)
                self.folder_index=0
            else:
                qt.QMessageBox.information(self,_("error"),_("no media files in this folder"))
        else:
            media = self.instance.media_new(text)
            self.player.set_media(media)
            self.player.play()
            self.path=text
            self.type="file or link"
            self.MF.setDisabled(True)
    def oninfo(self):
        qt.QMessageBox.information(self,_("file info"),_("media type {} current file {} current volume {} curren rate {} elapsed time {} remaining time {} duration {}").format(self.type,self.path,str(self.player.audio_get_volume()),str(self.player.get_rate()),self.timeformat(self.getdu(self.player.get_time())),self.timeformat(self.getdu(self.player.get_length()-self.player.get_time())),self.timeformat(self.getdu(self.player.get_length()))))
    def timeformat(self,time):
        t=[]
        if time[0]==0:
            pass
        else:
            t.append(_(" {} hours").format(str(time[0])))
        if time[1]==0:
            pass
        else:
            t.append(_(" {} minutes").format(str(time[1])))
        t.append(_(" {} seconds").format(str(time[2])))
        return " ".join(t)
    def ostop(self):
        if self.player.get_state()!=vlc.State.Ended:
            if self.player.is_playing():
                self.player.pause()
        else:
            media = self.instance.media_new(self.path)
            self.player.set_media(media)
        self.player.set_time(0)
    def ofolder(self):
        dialog = qt.QFileDialog()
        dialog.setFileMode(qt.QFileDialog.FileMode.Directory)
        if dialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            self.getFiles(dialog.selectedFiles()[0])
            if len(self.folder_files)>0:
                self.playMedia(os.path.join(self.folder_path,self.folder_files[0]))
                self.MF.setDisabled(False)
                self.folder_index=0
            else:
                qt.QMessageBox.information(self,_("error"),_("no media files in this folder"))
    def getFiles(self,path):
        l=os.listdir(path)
        self.folder_path=path
        self.folder_files=[]
        formats=['mp3','mp4','ogg','m4a','wav','occ']
        for file in l:
            for format in formats:
                if file.endswith(format):
                    self.folder_files.append(file)
                    break
        return self.folder_files
    def playMedia(self,path):
        media = self.instance.media_new(path)
        self.player.set_media(media)
        self.player.play()
        self.path=path
        self.type="folder"
    def control(self,i):
        if i==0:
            if self.folder_index==len(self.folder_files)-1:
                a=0
            else:
                a=self.folder_index+1
        elif i==1:
            if self.folder_index==0:
                a=len(self.folder_files)-1
            else:
                a=self.folder_index-1
        elif i==2:
            a=0
        elif i==3:
            a=len(self.folder_files)-1
        self.playMedia(os.path.join(self.folder_path,self.folder_files[a]))
        self.MF.setDisabled(False)
        self.folder_index=a
App=qt.QApplication([])
w=main()
w.show()
App.exec()