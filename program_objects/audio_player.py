from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QWidget, QPushButton, QSlider,QHBoxLayout

class AudioPlayer(QWidget):
	"""
	This class represent the audio player widget.
	"""
	def __init__(self) -> None:
		super().__init__()
		self.init_ui()
		self.init_player()
		self.init_signals()

	def init_ui(self) -> None:
		"""
		This method create the audio player ui.
		"""
		self.setStyleSheet("QPushButton{qproperty-iconSize: 25px;}")
		h_layout = QHBoxLayout()
		self.play_pause_btn = QPushButton()
		self.play_pause_btn.setObjectName("play")
		self.play_pause_btn.setIcon(QIcon("style\\icons\\play.png"))
		self.stop_btn = QPushButton("")
		self.stop_btn.setIcon(QIcon("style\\icons\\stop.png"))
		self.slider = QSlider()
		self.slider.setOrientation(Qt.Orientation.Horizontal)
		self.plus_btn = QPushButton("")
		self.plus_btn.setIcon(QIcon("style\\icons\\plus.png"))
		self.minus_btn = QPushButton("")
		self.minus_btn.setIcon(QIcon("style\\icons\\minus.png"))

		h_layout.addWidget(self.play_pause_btn,1/3)
		h_layout.addWidget(self.stop_btn,1/3)
		h_layout.addWidget(self.slider,20)
		h_layout.addWidget(self.minus_btn, 1/3 )
		h_layout.addWidget(self.plus_btn, 1/3 )
		
		self.setLayout(h_layout)
	
	def init_player(self) -> None:
		"""
		This method create the media player
		"""
		self.player = QMediaPlayer()
		self.audio = QAudioOutput()
		self.player.setAudioOutput(self.audio)

	def init_signals(self) -> None:
		"""
		This method define the signals.
		"""	
		self.play_pause_btn.clicked.connect(self.play)
		self.stop_btn.clicked.connect(self.stop)
		self.player.positionChanged.connect(self.update_slider)
		self.player.durationChanged.connect(self.update_slider_values)
		self.player.mediaStatusChanged.connect(self.audio_finished)
		
		
		self.plus_btn.clicked.connect(self.plus)
		self.minus_btn.clicked.connect(self.minus)
	
	def update_slider_values(self) -> None:
		"""
		This method update the slider values according the audio duration.
		"""
		self.slider.setRange(0, self.player.duration())
		self.slider.setValue(0)

	def play(self) -> None:
		"""
		This method is called when play button is clicked.
		"""
		self.update_slider_values()

		if self.play_pause_btn.objectName()  == "play":
			self.play_pause_btn.setIcon(QIcon("style\\icons\\pause.png"))
			self.play_pause_btn.setObjectName("pause")
			self.player.play()
		else:
			self.play_pause_btn.setObjectName("play")
			self.play_pause_btn.setIcon(QIcon("style\\icons\\play.png"))
			self.player.pause()
	
	def stop(self) -> None:
		"""
		This method is called when stop button is clicked.
		"""
		self.play_pause_btn.setIcon(QIcon("style\\icons\\play.png"))
		self.play_pause_btn.setObjectName("play")
		self.player.stop()
		self.slider.setValue(0)

	def update_slider(self, position) -> None:
		"""
		This method is called when audio position change and update the slider value.

		Args:
			position : the player current position.
		"""
		self.slider.setValue(position)

	def plus(self) -> None:
		"""
		This method is called when jump forward button is clicked.
		"""
		self.player.setPosition(self.player.position() + int(self.player.duration() * 0.2))

	def minus(self) -> None:
		"""
		This method is called when jump backward button is clicked.
		"""
		self.player.setPosition(self.player.position() - int(self.player.duration() * 0.2))
	
	def audio_finished(self, media_status) -> None:
		"""
		This method is called when media status changes.

		Args:
			media_status : current media status.
		"""
		if media_status == QMediaPlayer.MediaStatus.EndOfMedia:
			self.play_pause_btn.setObjectName("play")
			self.play_pause_btn.setIcon(QIcon("style\\icons\\play.png"))
			self.slider.setValue(0)
		if media_status == QMediaPlayer.MediaStatus.LoadedMedia:
			self.play_pause_btn.setObjectName("play")
			self.play_pause_btn.setIcon(QIcon("style\\icons\\play.png"))
			self.slider.setValue(0)

