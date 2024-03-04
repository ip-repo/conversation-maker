from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from program_objects.conversation_maker import ConversationMaker

#entry point

if __name__ == "__main__":
	app = QApplication([])
	app.setWindowIcon(QIcon("style\\icons\\app.png"))
	with open("style\\style-sheet\\style.qss", "r") as style_file:
		style = style_file.read()
	with open("program_objects\\welcome.txt", "r") as welcome_file:
		text = welcome_file.read()
	app.setStyleSheet(style)
	main_window = ConversationMaker()
	main_window.text_edit.setText(text)
	main_window.show()
	app.exec()
