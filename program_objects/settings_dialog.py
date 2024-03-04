import requests
import pyttsx3
import gtts.langs, gtts.accents
from program_objects.workers import SampleWorker
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import (QLineEdit, QDialog,QDialogButtonBox, QHBoxLayout,QVBoxLayout,
							   QComboBox,QCheckBox,QLabel,QDoubleSpinBox,QPushButton)




class SettingsDialog(QDialog):
	"""
	This class is dialog that allow user do pick different values.
	"""
	def __init__(self, parent=None) -> None:
		super(SettingsDialog, self).__init__(parent)
		self.init_ui()
		self.init_objects_and_signals()
		result = self.test_connection()
		if result == False:
			self.gtts_sample_btn.setDisabled(True)
			self.gtts_sample_btn.setToolTip("No internet connection so gtts cannot work.\nif you have reconnected to the internet open this settings dialog again.")
			self.gtts_sample_btn.setStyleSheet("color:red;")
	
	def init_ui(self) -> None:
		"""
		This method init the ui.
		"""
		self.pytts_label = QLabel("pyttsx3 default: ")
		self.pytts_voice = QComboBox()
		self.pytts_rate = QDoubleSpinBox()
		self.pytts_rate.setToolTip("set rate")
		self.pytts_volume = QDoubleSpinBox()
		self.pytts_volume.setToolTip("set volume")
		self.pytts_sample_btn = QPushButton("sample")

		self.gtts_label = QLabel("gtts default: ")
		self.gtts_lang = QComboBox()
		self.gtts_accents = QComboBox()
		self.gtts_slow = QCheckBox("slow")
		self.gtts_sample_btn = QPushButton("sample")
		
		self.line_edit = QLineEdit("Example")
		self.add_sample = QComboBox()
		
		self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		
		h_layout_sample_pytts = QHBoxLayout()
		h_layout_sample_pytts.addWidget(self.pytts_label ,1)
		h_layout_sample_pytts.addWidget(self.pytts_voice ,1)
		h_layout_sample_pytts.addWidget(self.pytts_rate ,1)
		h_layout_sample_pytts.addWidget(self.pytts_volume ,1)
		h_layout_sample_pytts.addWidget(self.pytts_sample_btn,1)

		h_layout_sample_gtts = QHBoxLayout()
		h_layout_sample_gtts.addWidget(self.gtts_label ,1)
		h_layout_sample_gtts.addWidget(self.gtts_slow ,1)
		h_layout_sample_gtts.addWidget(self.gtts_lang ,1)
		h_layout_sample_gtts.addWidget(self.gtts_accents ,1)
		h_layout_sample_gtts.addWidget(self.gtts_sample_btn, 1)

		line_layout = QHBoxLayout()
		line_layout.addWidget(self.line_edit, 4)
		line_layout.addWidget(self.add_sample, 1)

		v_layout = QVBoxLayout()
		v_layout.addLayout(h_layout_sample_pytts, 1)
		v_layout.addLayout(h_layout_sample_gtts, 1)
		v_layout.addLayout(line_layout, 1)
		v_layout.addWidget(self.button_box, 1, Qt.AlignmentFlag.AlignCenter)
		
		self.setLayout(v_layout)
		self.setFixedHeight(150)
		self.setFixedWidth(600)
		self.setWindowTitle("settings")
		self.setWindowIcon(QIcon("style\\icons\\settings.png"))
		
	def init_objects_and_signals(self) -> None:
		"""
		This method init signals and important class objects.
		"""
		self.engine = pyttsx3.init()
		self.def_values = {"pyttsx3" : {"voice" : 0,
							 "volume": 1.0 , "rate" : 150 },
						"gtts" : {"lang" : "en", "tld" : "com", "slow" : False},
						"text" : "example", "add" : "none"}

		self.pytts_voice.addItems([voice.name for voice in self.engine.getProperty("voices")])
		self.pytts_rate.setRange(0.0, 200.0)
		self.pytts_rate.setValue(150.0)
		self.pytts_volume.setRange(0.0, 10.0)
		self.pytts_volume.setValue(10.0)
		self.gtts_lang.setMaxVisibleItems(5)
		self.gtts_lang.addItems(gtts.langs._langs.values())
		self.gtts_accents.addItems(gtts.accents.accents)
		self.add_sample.addItems(["none" ,"both" ,"pyttsx3" ,"gtts"])
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)
		self.pytts_sample_btn.clicked.connect(self.pytts_sample)
		self.gtts_sample_btn.clicked.connect(self.gtts_sample)

		self.thread_pool = QThreadPool()
	
	def update_def_values(self):
		"""
		This method of the values so that they can be fetched by the main program.
		"""
		self.def_values["pyttsx3"]["voice"] = self.pytts_voice.currentIndex()
		self.def_values["pyttsx3"]["volume"] = self.pytts_volume.value() / 10.0
		self.def_values["pyttsx3"]["rate"] = self.pytts_rate.value()
		self.def_values["gtts"]["lang"] = self.gtts_lang.currentText()
		self.def_values["gtts"]["tld"] = self.gtts_accents.currentText()
		self.def_values["gtts"]["slow"] = self.gtts_slow.isChecked()
		self.def_values["text"] = self.line_edit.text()
		self.def_values["add"] = self.add_sample.currentText()
		
		
	def accept(self) -> None:
		"""
		This method is called when user click ok.
		"""
		self.update_def_values()
		del self.engine
		self.done(1)
	
	def reject(self) -> None:
		"""
		This method is called when user click cancel.
		"""
		del self.engine
		self.done(-1)

	def close(self) -> bool:
		"""
		This method is called when dialog is closed.
		"""
		del self.engine
		return super().close()
	
	def get_def_values(self) -> dict:
		"""
		get the default engines new values.

		Returns:
			dict : default engine valiues.
		"""
		return self.def_values
	
	def pytts_sample(self) -> None:
		"""
		Start pytts worker to play the sample.
		"""
		if self.line_edit.text():
			self.gtts_sample_btn.setDisabled(True)
			self.pytts_sample_btn.setDisabled(True)
			self.button_box.setDisabled(True)
			sample_worker = SampleWorker("pyttsx3",self.line_edit.text(),self.pytts_voice.currentIndex(), int(self.pytts_rate.value()), self.pytts_volume.value() / 10.0)
			self.thread_pool.start(sample_worker)
			sample_worker.signals.finished.connect(self.pytts_worker_finished)
	
		

	def gtts_sample(self):
		"""
		Start gtts worker to play the sample.
		"""
		if self.line_edit.text():
			self.gtts_sample_btn.setDisabled(True)
			self.pytts_sample_btn.setDisabled(True)
			self.button_box.setDisabled(True)
			lang = None
			for key, value in gtts.langs._langs.items():
				if value == self.gtts_lang.currentText():
					lang = key
			sample_worker = SampleWorker("gtts",self.line_edit.text(), lang, self.gtts_accents.currentText(),self.gtts_slow.isChecked())
			self.thread_pool.start(sample_worker)
			sample_worker.signals.finished.connect(self.gtts_worker_finished)
			
	def gtts_worker_finished(self,message):
		"""
		This method is called when gtts worker is done.
		"""
		self.gtts_sample_btn.setEnabled(True)
		self.pytts_sample_btn.setEnabled(True)
		self.button_box.setEnabled(True)
	
	def pytts_worker_finished(self, message):
		"""
		This method is called when pytts worker is done.
		"""
		self.gtts_sample_btn.setEnabled(True)
		self.pytts_sample_btn.setEnabled(True)
		self.button_box.setEnabled(True)

	def test_connection(self):
		"""
		This method check for internet connection. 
		This is needed because to use gtts you need internet connection.
		"""
		try:
			x = requests.get("https://google.com")
			print(x.status_code)
			return True
		except requests.exceptions.ConnectionError:
			return False
		...
