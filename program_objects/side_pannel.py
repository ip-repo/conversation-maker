
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton


class SidePannel(QWidget):
	"""
	This class is the side pannel with the buttons.
	"""
	def __init__(self) -> None:
		super().__init__()
		self.init_ui()
		self.setFixedWidth(60)
		
	def init_ui(self) -> None:
		"""
		This method init the ui.
		"""
		self.settings_btn = QPushButton()
		self.settings_btn.setToolTip("settings")
		self.settings_btn.setIcon(QPixmap("style\\icons\\settings.png"))
		
		self.add_pytts_btn = QPushButton()
		self.add_pytts_btn.setToolTip("add pyttsx3")
		self.add_pytts_btn.setIcon(QPixmap("style\\icons\\char1.png"))
		self.add_gtts_btn = QPushButton()
		self.add_gtts_btn.setToolTip("add gtts")
		self.add_gtts_btn.setIcon(QPixmap("style\\icons\\char2.png"))
		self.clear_btn = QPushButton()
		self.clear_btn.setToolTip("clear text")
		self.clear_btn.setIcon(QPixmap("style\\icons\\clear.png"))
		self.save_text_btn = QPushButton()
		self.save_text_btn.setToolTip("save text")
		self.save_text_btn.setIcon(QPixmap("style\\icons\\savetxt.png"))
		self.space_label = QLabel()
		self.run_btn = QPushButton()
		self.run_btn.setToolTip("generate speech")
		self.run_btn.setIcon(QPixmap("style\\icons\\run.png"))

		v_layout = QVBoxLayout()
		v_layout.addWidget(self.settings_btn, 1)
		v_layout.addWidget(self.add_pytts_btn, 1)
		v_layout.addWidget(self.add_gtts_btn, 1)
		v_layout.addWidget(self.save_text_btn, 1)
		v_layout.addWidget(self.clear_btn, 1)
		v_layout.addWidget(self.space_label, 1)
		v_layout.addWidget(self.run_btn, 1)
		self.setLayout(v_layout)

