import NBSapi
tts=NBSapi.NBSapi()
import guiTools
import gtts
from guiTools.dictionarys import languages
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
import language
language.init_translation()
class TextToSpeech (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("text to speach"))
        self.p=p
        layout1=qt.QVBoxLayout()
        self.serves=guiTools.comboBook(layout1,_("select serves"))
        self.text=qt.QLineEdit()
        self.text.setAccessibleName(_("text"))
        self.lang=qt.QComboBox()
        self.lang.setAccessibleName(_("select language"))
        self.lang.addItems(['Albanian', 'Arabic', 'Bosnian', 'Bulgarian', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Finnish', 'French', 'German', 'Gujarati', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Khmer', 'Korean', 'Latvian', 'Lithuanian', 'Malay', 'Malayalam', 'Nepali', 'Norwegian', 'Polish', 'Portuguese', 'Russian', 'Slovak', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Ukrainian', 'Urdu', 'Vietnamese', 'Welsh'])
        self.save=qt.QPushButton(_("save"))
        self.save.clicked.connect(self.fsave)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.lang)
        layout.addWidget(self.save)
        self.serves.add(_("google"),layout)
        self.setLayout(layout1)
    def fsave(self):
        file=qt.QFileDialog(self)
        file.setDefaultSuffix("mp3")
        file.setAcceptMode(qt.QFileDialog.AcceptMode.AcceptSave)
        file.setNameFilters(["audio files(*.mp3)"])
        if file.exec() == qt.QFileDialog.DialogCode.Accepted:
            google(self.text.text(),file.selectedFiles()[0],languages[self.lang.currentText()])
            m=qt.QMessageBox()
            m.setText(_("file saved successfully \n do you want to  play it ?"))
            m.setWindowTitle(_("done"))
            b1=m.addButton(qt.QMessageBox.StandardButton.Yes)
            b1.setText(_("play file"))
            b2=m.addButton(qt.QMessageBox.StandardButton.No)
            b2.setText(_("cloce"))
            m.exec()
            x=m.clickedButton()
            if x==b1:
                media = self.p.instance.media_new(file.selectedFiles()[0])
                self.p.player.set_media(media)
                self.p.player.play()
                self.p.path=file.selectedFiles()[0]
                self.p.type="tts file"
            self.close()


def google(text,fileName,language):
    s=gtts.gTTS(text,lang=language)
    s.save(fileName)
def getrate():
    return tts.GetRate()
def getv():
    return tts.GetVolume()
def getvoicesL():
    l=[]
    v=tts.GetVoices()
    for voice in v:
        l.append(voice["Description"])
    return l
def save(text,rate,volume,voice,path):
    tts.SetRate(rate)
    tts.SetVolume(volume)
    tts.SetVoice(voice,"by_description")
    tts.SpeakToFile(text,path,0)