from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from pydub import AudioSegment
import pyttsx3,shutil,os
from gtts import gTTS
import gtts.langs
import sys
from pydub.playback import play

class SampleWorker(QRunnable):
	"""
	This worker job is to play the smaples in settings dialog.
	"""
	def __init__(self, *args):
		super(SampleWorker, self).__init__()
		self.signals = Signals()
		self.engine = args[0]
		self.temp_folder = "sample-temp"
	
		if self.engine == "pyttsx3":
			self.text = args[1]
			self.voice = args[2]
			self.rate = args[3]
			self.volume = args[4]
		else:
			self.text = args[1]
			self.lang = args[2]
			self.tld = args[3]
			self.slow = args[4]
		...
	@Slot()
	def run(self) -> None:
		"""
		This method is called when wokrer is started.
		"""
		engine = pyttsx3.init()
		if self.engine == "pyttsx3":
			engine.setProperty("voice", engine.getProperty("voices")[self.voice].id)
			engine.setProperty("rate", self.rate)
			engine.setProperty("volume",self.volume)
			engine.say(self.text)
			engine.runAndWait()
		else:
			if os.path.exists(self.temp_folder):
				shutil.rmtree(self.temp_folder)
				os.mkdir(self.temp_folder)
			else:
				os.mkdir(self.temp_folder)

			tts = gTTS(text=self.text, lang=self.lang, tld=self.tld, slow=self.slow)
			tts.save("{}\\sample.mp3".format(self.temp_folder))
			audio_seg = AudioSegment.from_mp3("{}\\sample.mp3".format(self.temp_folder))
			play(audio_seg)
			shutil.rmtree(self.temp_folder)
		self.signals.finished.emit("done")


class Worker(QRunnable):
	"""
	This worker get the user text speech and turn 
	it into a speech and save it as audio file.
	"""
	def __init__(self, *args):
		super(Worker, self).__init__()
		self.signals = Signals()
		self.pytts_parts = args[0]
		self.gtts_parts = args[1]
		self.file_name = args[2]

		self.format = args[3].split(" ")[1][3:-1]
	
		self.temp_folder = "temp"
		self.engine = pyttsx3.init()
		self.general = {}
	


	@Slot()
	def run(self) -> None:
		"""
		This method is called when wokrer is started.
		"""
		try:
			self.prepare_temp_folder()
			for part in self.pytts_parts:
				index = part[0]
				settings = part[1][0][7: ].split(":")
				lines = part[1][1: ]
				self.engine.setProperty("voice", self.engine.getProperty("voices")[int(settings[1])].id)
				self.engine.setProperty("rate", int(float(settings[2])))
				self.engine.setProperty("volume",float(settings[3]))
				self.engine.save_to_file(text=" ".join(lines), filename="{}\\{}.{}".format(self.temp_folder,index ,self.format))
				self.engine.runAndWait()
				self.general[index] = "{}\\{}.{}".format(self.temp_folder, index, self.format)
				self.engine.runAndWait()
			
			for part in self.gtts_parts:
				index = part[0]
				settings = part[1][0][7: ].split(":")
				lines = part[1][1: ]
				lang = None
				for key, value in gtts.langs._langs.items():
					if value == settings[1]:
						lang = key
				if settings[3] == "True":
					slow = True
				else:
					slow = False
				engine =gTTS(text=" ".join(lines),tld=settings[2],lang=lang,slow=slow)
				engine.save("{}\\{}.{}".format(self.temp_folder, index, self.format))
				self.general[index] = "{}\\{}.{}".format(self.temp_folder, index, self.format)

			self.create_output()
		except:
			exetype, value = sys.exc_info()[:2]
			self.signals.error.emit((exetype, value))
			try:
				shutil.rmtree(self.temp_folder)
			except:
				...
			
	

	def prepare_temp_folder(self):
		"""
		This method create a temporary place to holds the converted conversation parts.
		"""
		if os.path.exists(self.temp_folder):
			shutil.rmtree(self.temp_folder)
			
			os.mkdir(self.temp_folder)
		else:
			os.mkdir(self.temp_folder)

	def create_output(self):
		"""
		This method take the converted conversation parts and turn it into a singel audio file.
		"""
		combined = AudioSegment.empty()
		for key in sorted(self.general.keys()):

			sound = AudioSegment.from_file(self.general[key])
			combined += sound
		combined.export(self.file_name, format=self.format)
		shutil.rmtree(self.temp_folder)
		self.signals.finished.emit(self.file_name)
	

class Signals(QObject):
	"""
	Workers signals.
	"""
	finished = Signal(str)
	error = Signal(tuple)
	result = Signal(object)



