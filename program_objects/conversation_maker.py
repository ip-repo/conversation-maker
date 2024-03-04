
import pyttsx3
import gtts.langs, gtts.accents
import requests
from PySide6.QtWidgets import  (QWidget,QFileDialog, QHBoxLayout,QVBoxLayout,QTextEdit,
								 QFontComboBox,QDoubleSpinBox)
from PySide6.QtCore import  QThreadPool, QUrl
from program_objects.side_pannel import SidePannel
from program_objects.settings_dialog import SettingsDialog
from program_objects.workers import Worker
from program_objects.audio_player import AudioPlayer
from program_objects.info_dialog import InfoDialog




class ConversationMaker(QWidget):
	"""
	This widget allow user to create a conversation and convert it to speech.
	"""
	def __init__(self) -> None:
		super().__init__()
		self.init_ui()
		self.init_objects_and_signals()
			
	def init_ui(self) -> None:
		"""
		This method init the ui.
		"""	
		self.side_pannel = SidePannel()
		self.font_box = QFontComboBox()
		self.font_size_box = QDoubleSpinBox()
		self.font_size_box.setRange(1, 200)
		self.font_size_box.setValue(30)
		self.text_edit = QTextEdit()
		self.audio_widget = AudioPlayer()
		self.audio_widget.setDisabled(True)
		self.text_edit.setFontPointSize(30)
		h_layout = QHBoxLayout()
		v_layout = QVBoxLayout()
		font_layout = QHBoxLayout()
		
		font_layout.addWidget(self.font_box, 8)
		font_layout.addWidget(self.font_size_box ,2)
		v_layout.addWidget(self.audio_widget, 1)
		v_layout.addLayout(font_layout, 1)
		v_layout.addWidget(self.text_edit, 9)
		
		h_layout.addWidget(self.side_pannel, 1)
		h_layout.addLayout(v_layout,9)
		self.font_box.currentFontChanged.connect(self.text_edit.setFont)
		self.setWindowTitle("Conversation Maker")
		self.setLayout(h_layout)
		self.setMinimumHeight(500)
		self.setMinimumWidth(900)
	
	def init_objects_and_signals(self) -> None:
		"""
		This method init important objects and signals.
		"""
		engine = pyttsx3.init()
		self.counter = 1
		self.file_dialog = QFileDialog()
		self.thread_pool = QThreadPool()
		self.settings_data = {"pyttsx3" : {"voice" : 0,
							 "volume": 1.0 , "rate" : 150 },
						"gtts" : {"lang" : "English", "tld" : "com", "slow" : False}}
		
		del engine
		self.side_pannel.settings_btn.clicked.connect(self.update_settings)
		self.side_pannel.add_pytts_btn.clicked.connect(self.add_pytts)
		self.side_pannel.add_gtts_btn.clicked.connect(self.add_gtts)
		self.side_pannel.clear_btn.clicked.connect(self.clear_text)
		self.side_pannel.run_btn.clicked.connect(self.generate_audio_manager)		
		self.font_size_box.valueChanged.connect(self.update_font_size)
		self.side_pannel.save_text_btn.clicked.connect(self.save_text)
	
	def update_font_size(self, value)-> None:
		"""
		This method is called when user want to change font size.
		"""
		text = self.text_edit.toPlainText()
		self.text_edit.setFontPointSize(float(value))
		self.text_edit.clear()
		self.text_edit.setText(text)
	
	def update_settings(self) -> None:
		"""
		This method is called when user click the settings button.
		"""
		dialog = SettingsDialog()
		result  = SettingsDialog.exec(dialog)
		if result:
			new_settings_data = dialog.get_def_values()
			self.settings_data["pyttsx3"] = new_settings_data["pyttsx3"]
			self.settings_data["gtts"] = new_settings_data["gtts"]
			if new_settings_data["add"] == "pyttsx3":
				text = "[start]pyttsx3:" 
				text += str(new_settings_data["pyttsx3"]["voice"]) + ":"
				text += str(int(new_settings_data["pyttsx3"]["rate"])) + ":"
				text += str(new_settings_data["pyttsx3"]["volume"]) + ":"
				text += "\n" + str(new_settings_data["text"])
				self.text_edit.append(text)
			elif new_settings_data["add"] == "gtts":
				text = "[start]gtts:"
				text += new_settings_data["gtts"]["lang"] + ":"
				text += new_settings_data["gtts"]["tld"] + ":"
				text += str(new_settings_data["gtts"]["slow"]) + ":"
				text += "\n" + str(new_settings_data["text"])
				self.text_edit.append(text)
			elif new_settings_data["add"] == "both":
				text = "[start]pyttsx3:" 
				text += str(new_settings_data["pyttsx3"]["voice"]) + ":"
				text += str(int(new_settings_data["pyttsx3"]["rate"])) + ":"
				text += str(new_settings_data["pyttsx3"]["volume"]) + ":"
				text += "\n" + str(new_settings_data["text"]) +"\n"
				text += "[start]gtts:" 
				text += new_settings_data["gtts"]["lang"] + ":"
				text += new_settings_data["gtts"]["tld"] + ":"
				text += str(new_settings_data["gtts"]["slow"]) + ":"
				text += "\n" + str(new_settings_data["text"])
				self.text_edit.append(text)	
			else:
				...

	def add_pytts(self) -> None:
		"""
		This method is called when user click add pyttsx3 button.
		"""
		text = "[start]pyttsx3:" 
		text += str(self.settings_data["pyttsx3"]["voice"]) + ":"
		text += str(int(self.settings_data["pyttsx3"]["rate"])) + ":"
		text += str(self.settings_data["pyttsx3"]["volume"]) + ":"
		self.text_edit.append(text)
	
	def add_gtts(self) -> None:
		"""
		This method is called when user click add gtts button.
		"""
		text = "[start]gtts:"
		text += self.settings_data["gtts"]["lang"] + ":"
		text += self.settings_data["gtts"]["tld"] + ":"
		text += str(self.settings_data["gtts"]["slow"]) + ":"
		self.text_edit.append(text)
	
	def test_if_command_in_text(self) ->str:
		"""
		This method is called when user want to turn speech to audio.
		It will check if the user has typed an accepted syntax.

		Returns:
			str : test result message.
		"""
		text = self.text_edit.toPlainText().strip()

		if text:
			self.audio_widget.setDisabled(True)
			lines = text.split("\n")
			for line in lines:
				if line.startswith("[start]"):
					return "start" 
				elif line.startswith("[help]"):
					return "help"
				else:
					return "no command"

	def find_start_indexs(self) -> list:
		"""
		This method find start commands indexs.

		Rerturns:
			list: start command indexs.
		"""
		text = self.text_edit.toPlainText().strip()	
		start_index = []
		if text:
			self.audio_widget.setDisabled(True)
			lines = text.split("\n")
			
			for i, line in enumerate(lines):
				if line.startswith("[start]"):
					start_index.append(i)
		return start_index
	
	def create_conversation_list(self, start_index: list) ->list:
		"""
		This method get the start indexs of start commands and find their matching text.
		
		Returns:
			list : a list of the conversation as parts.
		"""
		text = self.text_edit.toPlainText().strip()

		conversation_parts = []
		if text:
			lines = text.split("\n")
			while True:
				if len(start_index) == 0:
					break
				if len(start_index) == 1:
					conversation_parts.append(lines[start_index[0] : ])
					start_index = start_index[1:]
				else:
					conversation_parts.append(lines[start_index[0] : start_index[1]])
					start_index = start_index[1 : ]
		return conversation_parts
	
	def split_conversation_parts(self, conversation_parts: list) -> list:
		"""
		This method create two list of conversation parts to be sent to the workers.

		Reutrn:
			list : convertsation parts.
		"""
		pytts_to_convert = []
		gtts_to_convert = []
		index = 0
		for part in conversation_parts:
			print(part.count(":"))
			if len(part) == 1:
				continue
			else:			
				if part[0][7:].startswith("pyttsx3"):
					print(part[0][7:].split(":"))
					if part[0][7:].count(":") != 4:
						return [False, "number of : is not 4", part[0][7:]]
					if len(part[0][7:].split(":")) > 4 and (part[0][7:].split(":")[4]!=""):
						print(part[0][7:].split(":"))
						return [False, "start line syntax not correct", part[0][7:]]
					
					print(part[0][7:].split(":"))
					for i, setting in  enumerate(part[0][7:].split(":")[:4]):
						if setting:
							if i == 0:
								continue
							if i == 1:
								try:
									test = int(setting)
								except Exception as ec:
									print(ec,part[0][7:].split(":"))
									return [False, "setting is wrong" +part[0][7:], setting, i]
							if i == 2:
								try:
									test = int(setting)
								except Exception as ec:
									return [False, "setting is wrong",part[0][7:], setting, i]
							if i == 3:
								try:
									test = float(setting)
								except Exception as ec:
									return [False, "setting is wrong",part[0][7:], setting, i]
							if i == 4:
								return [False, "setting to long",part[0][7:], setting, i]
						else:
							print(setting)
							return [False, "setting is empty",part[0][7:]]
					pytts_to_convert.append([index, part])
					index +=1
					
				elif part[0][7:].startswith("gtts"):
					if part[0][7:].count(":") != 4:
						return [False, "number of : is not 4", part[0][7:]]
					if len(part[0][7:].split(":")) > 4  and (part[0][7:].split(":")[4]!=""):
						return [False, "start line syntax not correct", part[0][7:]] 
					for i, setting in  enumerate(part[0][7:].split(":")):
						if setting:
							if i == 0:
								continue
							if i == 1:
								if setting not in gtts.langs._langs.values():
									return [False, "language is not supported",part[0][7:], setting, i]
							if i == 2:
								if setting not in gtts.accents.accents:
									return [False, "tld is not supported",part[0][7:], setting, i]
							if i == 3:
								if setting not in ["True","False"]:
									return [False, "wrong slow value",part[0][7:], setting, i]

					gtts_to_convert.append([index, part])
					index +=1
				
				else:
					return [False, "conversation parts arrived with free lines",part]
					...
		if len(pytts_to_convert) == 0 and len(gtts_to_convert) == 0:
			return [False, [],[]]
		return [True,pytts_to_convert, gtts_to_convert]
	
	def remove_empty_lines(self, pytts_to_convert: list, gtts_to_convert: list) -> list:
		"""
		This method remove empty lines.

		Returns:
			list : a list with the parts the send to workers.
		"""
		new_pytts = []
		for part in pytts_to_convert:
			temp = [part[0]]
			lines = []
			for line in part[1]:
				if line:
					lines.append(line)
			temp.append(lines)
			new_pytts.append(temp)

		new_gtts = []
		for part in gtts_to_convert:
			temp = [part[0]]
			lines = []
			for line in part[1]:
				if line:
					lines.append(line)
			temp.append(lines)
			new_gtts.append(temp)
		return [new_pytts, new_gtts]
	
	def test_connection(self) -> bool:
		"""
		Test for internet connection.
		gtts require internet.

		Returns:
			bool: test result.
		"""
		try:
			res = requests.get("https://google.com")
			if res.status_code == 200:
				return True
			else:
				return False
		except requests.exceptions.ConnectionError:
			return False

	def start_thread_work(self, pytts:list, gtts:list) -> None:
		"""
		This method ask for user for a saving path for the speech
		and then send the conversation parts to convert to the matching workers.
		"""
		file_name, format = self.file_dialog.getSaveFileName(None,"Save speech as audio","output{}.mp3".format(self.counter),
												"MP3 (*.mp3);;WAV (*.wav);;")
		self.counter +=1
		if file_name:
			worker = Worker(pytts, gtts, file_name, format)
			self.thread_pool.start(worker)
			
			worker.signals.finished.connect(self.generation_is_finished)
			worker.signals.error.connect(self.handle_erros_in_generation)
		else:
			...
			#self.audio_widget.setEnabled(True)

	def generate_audio_manager(self) -> None:
		"""
		This method is called when user click run button.
		This method manages the tests and if there is problem it will alret user.
		"""
		result = self.test_if_command_in_text()
		if result == "start":
			start_indexs = self.find_start_indexs()
			if start_indexs:
				conversation_parts = self.create_conversation_list(start_index=start_indexs)
				if conversation_parts:
					result = self.split_conversation_parts(conversation_parts=conversation_parts)
					if result[0]:
						print(result)
						pytts_to_convert = result[1]
						gtts_to_convert = result[2]
						result = self.remove_empty_lines(pytts_to_convert=pytts_to_convert, gtts_to_convert=gtts_to_convert)
						pytts_final_list = result[0]
						gtts_final_list = result[1]
						connection_test = self.test_connection()
						if gtts_final_list:
							if connection_test == False:
								dialog = InfoDialog()
								dialog.label.setText("gtts require a internet connection. internet test has faild so conversaion generation is aborted.")
								result  = InfoDialog.exec(dialog)
								return
							

						self.start_thread_work(pytts=pytts_final_list, gtts=gtts_final_list)
						

						
					else:
						print(result)
						dialog = InfoDialog()
						
						dialog.label.setText( """Your command is wrong:\nCorrect examples:\n\t[start]pyttsx3:1:150:7.5:\n\tsome text\n\t[start]gtts:English:com:False:\n\tsome more text""")
						result  = InfoDialog.exec(dialog)
				else:
					dialog = InfoDialog()
					dialog.label.setText("failed: could not parse conversation into parts.")
					
					result  = InfoDialog.exec(dialog)

			else:
				dialog = InfoDialog()
				dialog.label.setText("could not find start command.. try this command: [help]")
				
				result  = InfoDialog.exec(dialog)

		
		elif result == "help":
			dialog = InfoDialog()
			dialog.help()
			
			result  = InfoDialog.exec(dialog)
		else:
			dialog = InfoDialog()
			dialog.label.setText("This is not right syntax: try this command for more information: [help]")
			
			result  = InfoDialog.exec(dialog)

	def handle_erros_in_generation(self,error: tuple):
		"""
		This method is called if the workers encounter a error.
		"""
		dialog = InfoDialog()
		dialog.label.setText( "Error during generation of speech process: " + str(error[0])+ str(error[1]))
		InfoDialog.exec(dialog)				
	
	def generation_is_finished(self,audio_path) -> None:
		"""
		This method is called when worker end his job.
		It will set the new audio file as the source for media player.
		"""
		self.audio_widget.setEnabled(True)
		self.audio_widget.player.setSource(QUrl(audio_path))
			
	def clear_text(self) -> None:
		"""
		This method is called when clear button is clicked.
		"""
		self.text_edit.clear()
		self.audio_widget.setDisabled(True)
	
	def save_text(self) -> None:
		"""
		This method is called when save text button is clicked.
		"""
		file_name, _ = self.file_dialog.getSaveFileName(None,"Save","conversation.txt",
												"TXT (*.txt);;")
		text = self.text_edit.toPlainText()
		if file_name and text:
			with open(file_name, "w") as file:
				file.write(text)
