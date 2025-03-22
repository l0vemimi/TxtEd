import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPlainTextEdit, QVBoxLayout, QWidget, QMenuBar
from PyQt6.QtGui import QIcon, QTextCharFormat, QColor, QTextCursor, QAction
from PyQt6.QtCore import Qt
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.styles import get_style_by_name
from pygments.token import Token

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TxtEd-QT')
        self.setGeometry(100, 100, 800, 600)

        self.text_area = QPlainTextEdit(self)
        self.setCentralWidget(self.text_area)

        self.createMenuBar()

        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name("default")

        self.text_area.textChanged.connect(self.syntax_highlight)

    def createMenuBar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('File')

        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.setPlainText(content)
                self.set_lexer(file_path)
                self.syntax_highlight()

    def save_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.toPlainText()
                file.write(content)

    def set_lexer(self, file_path):
        try:
            self.lexer = guess_lexer_for_filename(file_path, "")
        except Exception as e:
            self.lexer = get_lexer_by_name("text")

    def syntax_highlight(self):
        text = self.text_area.toPlainText()
        tokens = lex(text, self.lexer)

        self.text_area.blockSignals(True)
        cursor = self.text_area.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        self.text_area.setTextCursor(cursor)

        for token_type, token_value in tokens:
            start_index = text.find(token_value)
            end_index = start_index + len(token_value)
            cursor.setPosition(start_index)
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(token_value))
            char_format = QTextCharFormat()
            color = self.style.styles.get(token_type, "#000000")
            char_format.setForeground(QColor(color))
            cursor.setCharFormat(char_format)

        self.text_area.blockSignals(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())