# conversation-maker: turn text conversations to speech.

<img src="conversation-maker.png"></img>

A PySide6 text to speech program that allow user to create speech conversations from text conversations.
<hr>

### How to use:

When you open the program you will see a text area.

This text area is where the user can construct his conversation.<br>
Each conversation part should have a start command and text the will follow in the next line.

#### The syntax of a start command:<br>
Each start line should have exactly for settings and after a setting is it a most to add a : sign.<br>
The sart line command must have 4 : signs, one after each setting.

```console
[start]engine-name:settings-1:settings-2:setting-3:

```
gtts examples:
```console
[start]:gtts-str:language-str:accent(tld)-str:slow-str:
------------------------------------------------------
[start]gtts:English:com:False:
[start]gtts:Latin:com:True:
```
pyttsx3 examples:
```console
[start]pyttsx3-str:voice-index-int:rate-int:volume-float:

[start]pyttsx3:0:125:7.3:
[start]pyttsx3:1:70:10.0:
```
#### Help command
if you want to get more information about how to use the program type in text area **[help]**
and click on the run button and a window with help inforamtion will appear.

```console
[help]
```

### How to install:

This program use a few python modules so make sure to install them.
```console
git clone https://github.com/ip-repo/conversation-maker.git
python -m venv cm-venv #create a virtual environment 
cm-venv\Scripts\activate #activate venv
#required modules
pip install PySide6 #version: 6.6.2
pip install pyaudio #version 0.2.14
pip install pydub #version: 0.25.1
pip install gtts  #version: 2.5.1
pip install pyttsx3 #version 2.90
pip install requests #version: 2.31
cd conversation-maker #get into the project directory
python run.py

```
Or
```console
git clone https://github.com/ip-repo/conversation-maker.git
python -m venv cm-venv #create a virtual environment 
cm-venv\Scripts\activate #activate venv
cd conversation-maker #get into the project directory
pip install -r requirements.txt
python run.py

```
## A few notes:
- gtts require internet connection so if your offline you will be able to the use only pyttsx3 engine (the program will notify you).
- in order to avoid qmediaplayer conflicst please avoid of resaving a new speech file with the same name as a prior speech file( if the new file format isn't the same as an old one then it ok) if you dont follow this instruction the Slider in the program might not perform as expected.
- this program was made for windows, if you want to use it for linux make sure to changes path in workers.py and run.py
  
