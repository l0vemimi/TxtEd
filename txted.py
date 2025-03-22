#!/usr/bin/env python

import tkinter as tk
from tkinter import filedialog, Text

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Styled Text Editor")

        # Set window size and background color
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Customize text area
        self.text_area = Text(self.root, wrap='word', undo=True, font=("Helvetica", 14), bg="#ffffff", fg="#000000", insertbackground="black")
        self.text_area.pack(expand='yes', fill='both', padx=10, pady=10)

        # Customize menu bar
        self.menu_bar = tk.Menu(self.root, bg="#d3d3d3", fg="#000000")

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg="#d3d3d3", fg="#000000")
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.root.config(menu=self.menu_bar)

        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-c>', self.copy_text)
        self.root.bind('<Control-v>', self.paste_text)
        self.root.bind('<Control-x>', self.cut_text)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, content)

    def save_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def copy_text(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.selection_get())

    def paste_text(self, event=None):
        self.text_area.insert(tk.INSERT, self.root.clipboard_get())

    def cut_text(self, event=None):
        self.copy_text()
        self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

if __name__ == "__main__":
    root = tk.Tk()
    text_editor = TextEditor(root)
    root.mainloop()