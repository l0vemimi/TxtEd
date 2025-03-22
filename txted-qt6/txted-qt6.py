import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPlainTextEdit, QVBoxLayout, QWidget, QMenuBar, QHBoxLayout, QLabel, QStatusBar
from PyQt6.QtGui import QIcon, QTextCharFormat, QColor, QTextCursor, QAction, QFont, QPainter, QTextFormat, QKeySequence
from PyQt6.QtCore import Qt, QRect, QSize, QEvent
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.styles import get_style_by_name


class NumberBar(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')

    def update_width(self, _):
        width = self.fontMetrics().horizontalAdvance(str(self.editor.blockCount())) + 10
        self.editor.setViewportMargins(width, 0, 0, 0)
        self.setFixedWidth(width)

    def update_on_scroll(self, rect, dy):
        if dy:
            self.scroll(0, dy)
        else:
            self.update()
        if rect.contains(self.editor.viewport().rect()):
            self.update_width(0)

    def paintEvent(self, event):
        self.editor.blockCount()
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.GlobalColor.white)

        block = self.editor.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, top, self.width(), self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            blockNumber += 1

        painter.end()


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TxtEd-QT')
        self.setGeometry(100, 100, 800, 600)

        self.text_area = QPlainTextEdit(self)
        self.number_bar = NumberBar(self.text_area)

        layout = QHBoxLayout()
        layout.addWidget(self.number_bar)
        layout.addWidget(self.text_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.createMenuBar()

        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name("default")

        self.text_area.textChanged.connect(self.syntax_highlight)
        self.text_area.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.text_area.setFont(QFont("Courier", 10))

        # Word count at bottom corner
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.word_count_label = QLabel(self)
        self.word_count_label.setStyleSheet("color: grey;")
        self.status_bar.addPermanentWidget(self.word_count_label)
        self.update_word_count()

        # Shortcuts
        self.createShortcuts()

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
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def createShortcuts(self):
        copy_action = QAction(self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.text_area.copy)
        self.addAction(copy_action)

        paste_action = QAction(self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.text_area.paste)
        self.addAction(paste_action)

        cut_action = QAction(self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.text_area.cut)
        self.addAction(cut_action)

        select_all_action = QAction(self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.text_area.selectAll)
        self.addAction(select_all_action)

        zoom_in_action = QAction(self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+="))
        zoom_in_action.triggered.connect(self.zoom_in)
        self.addAction(zoom_in_action)

        zoom_out_action = QAction(self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        self.addAction(zoom_out_action)

    def zoom_in(self):
        font = self.text_area.font()
        size = font.pointSize()
        font.setPointSize(size + 1)
        self.text_area.setFont(font)

    def zoom_out(self):
        font = self.text_area.font()
        size = font.pointSize()
        font.setPointSize(max(size - 1, 1))
        self.text_area.setFont(font)

    def new_file(self):
        self.text_area.clear()
        self.update_word_count()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.setPlainText(content)
                self.set_lexer(file_path)
                self.syntax_highlight()
                self.update_word_count()

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)")
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
            while start_index != -1:
                end_index = start_index + len(token_value)
                cursor.setPosition(start_index)
                cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(token_value))
                char_format = QTextCharFormat()
                color = self.style.styles.get(token_type, "#000000")
                char_format.setForeground(QColor(color))
                cursor.setCharFormat(char_format)
                start_index = text.find(token_value, end_index)

        self.text_area.blockSignals(False)
        self.update_word_count()

    def update_word_count(self):
        text = self.text_area.toPlainText()
        words = text.split()
        word_count = len(words)
        self.word_count_label.setText(f"Word count: {word_count}")

    def eventFilter(self, obj, event):
        if obj == self.text_area and event.type() == event.Type.KeyRelease:
            self.update_word_count()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())