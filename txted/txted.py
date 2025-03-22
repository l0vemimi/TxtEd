import tkinter as tk
from tkinter import filedialog, Text
from pygments import lex
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.styles import get_style_by_name
from pygments.token import Token

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("simple text editor")

        # set window size and background color
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        # customise text area
        self.text_area = Text(self.root, wrap='word', undo=True, font=("Helvetica", 14), bg="#ffffff", fg="#000000", insertbackground="black")
        self.text_area.pack(expand='yes', fill='both', padx=10, pady=10)

        # word count label
        self.word_count_label = tk.Label(self.root, text="Word count: 0", bg="#f0f0f0", font=("Helvetica", 12))
        self.word_count_label.pack(side='bottom', pady=5)

        # customise menu bar
        self.menu_bar = tk.Menu(self.root, bg="white", fg="#000000")

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg="white", fg="#000000")
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.root.config(menu=self.menu_bar)

        # bind keyboard shortcuts
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-c>', self.copy_text)
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-x>', self.cut_text)

        # bind ext change event to update word count and syntax highlighting
        self.text_area.bind('<KeyRelease>', self.update_word_count)
        self.text_area.bind('<KeyRelease>', self.syntax_highlight)

        # initial lexer
        self.lexer = get_lexer_by_name("python")
        self.style = get_style_by_name("default")

        # initial syntax highlighting
        self.syntax_highlight()

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.update_word_count()
        self.syntax_highlight()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                            filetypes=[("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, content)
                self.update_word_count()
                self.set_lexer(file_path)
                self.syntax_highlight()

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def copy_text(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.selection_get())

    def paste_text(self, event=None):
        self.text_area.insert(tk.INSERT, self.root.clipboard_get())
        self.update_word_count()
        self.syntax_highlight()

    def cut_text(self, event=None):
        self.copy_text()
        self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.update_word_count()
        self.syntax_highlight()

    def update_word_count(self, event=None):
        text = self.text_area.get(1.0, tk.END)
        words = text.split()
        word_count = len(words)
        self.word_count_label.config(text=f"Word count: {word_count}")

    def set_lexer(self, file_path):
        try:
            self.lexer = guess_lexer_for_filename(file_path, "")
        except Exception as e:
            self.lexer = get_lexer_by_name("text")

    def syntax_highlight(self, event=None):
        # Remove previous tags
        for tag in self.text_area.tag_names():
            self.text_area.tag_delete(tag)

        # Get the text from the text area
        text = self.text_area.get(1.0, tk.END)

        # Get tokens from the text
        tokens = lex(text, self.lexer)

        # Apply tags based on tokens
        for token_type, token_value in tokens:
            if token_type in Token:
                start_index = f"1.0 + {text.index(token_value)} chars"
                end_index = f"1.0 + {text.index(token_value) + len(token_value)} chars"
                self.text_area.tag_add(str(token_type), start_index, end_index)

                # Get the color for the token type
                color = self.style.styles.get(token_type, "#000000")
                self.text_area.tag_config(str(token_type), foreground=color)

if __name__ == "__main__":
    root = tk.Tk()
    text_editor = TextEditor(root)
    root.mainloop()