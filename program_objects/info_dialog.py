from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel,QHBoxLayout

class InfoDialog(QDialog):
    """
    This class is the info dialog that pop when user ask for help or there a error.
    """
    def __init__(self, parent=None):
        super(InfoDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        This method init the ui/
        """
        self.label = QLabel("Info text.")
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label, 3)

        self.setLayout(h_layout)
        self.setWindowTitle("Info")
        self.setWindowIcon(QIcon("style\\icons\\info.png"))

    
    def help(self):
        """
        Set help text.
        """
        self.help_text = """This program allow to transform a written conversaion where each conversation part is handeld as
        an individual part when that text is converted to speech this allow to use different tts engines and settings for each part.
        When the user click on the run button (red arrow) the program check the text syntax and if it is correct 
        then it will generate a audio file containing the conversation  as speech according to user  desired saving path.

        The correct syntax of a command line should look like this:
        \t[start]enginename:engine-setting1:engine-setting2:engine-setting3:
        \t Note: all settings most be delcared and cannot remain empty!(NOT CORRECT-> [start]enginename::engine-setting2::)
        \t Note: in a command line most have only 4 ':' signs.
        There are two available engines:
        \t1.pyttsx3: -> [start]pyttsx3:voice:rate:volume:
        Examples:
        \t[start]pyttsx3:0:60:4.3;
        \t[start]pyttsx3:1:200:10.0;
        \t\tsettings:
        \t\t\tvoice: str(int) ,[0,1]  - available voices depend on voices installed on the user windows os (usally there 2 voices).
        \t\t\trate:  str(float) from 0 to 200 - you can use a higer rate but it will be to fast.
        \t\t\tvolume:str(float) from 0.0 to 10.0
        \t2.gtts: -> [start]gtts:language:accent:slow: (GTTS REQUIRE INTERNET CONNECTION!)
        Examples:
        \t[start]gtts:English:com:True;
        \t[start]gtts:Latin:com:False;
        \t\tsettings:
        \t\t\tlang: str() ,gtts.langs - available languages (you can see them under settings).
        \t\t\ttld: str()   ,gtts.accents - available accents a.k.a tld (you can see them under settings).
        \t\t\tslow: str(bool) ,[True,False] - slower speech.

        Buttons:
        \tColorful circles: this is the settings button.
        \tBlue characther: this will add to text edit the default pyttsx3 start command line (can be changed in settings).
        \tBrown characther: this will add to text edit the default gtts start command line (can be changed in settings).
        \tWhite border round square: this will allow user to save the text as text file.
        \tYellow border round square: this will allow user to clear the text edit.
        \tRed arrow: conversation to speech generate button. This will allow user to save the conversation as speech.
        """
        self.label.setText(self.help_text)
  
