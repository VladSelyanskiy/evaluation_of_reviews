from usage_of_models import use_model_nb, use_model_lr, tokenize_sentence

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

root = tk.Tk()
root.title("Макет")
root.geometry("600x300")

root.grid_rowconfigure(index=0, weight=1)
root.grid_rowconfigure(index=1, weight=1)
root.grid_rowconfigure(index=2, weight=1)
root.grid_rowconfigure(index=4, weight=1)
root.grid_rowconfigure(index=5, weight=1)
root.grid_rowconfigure(index=6, weight=1)
root.grid_rowconfigure(index=7, weight=1)
root.grid_rowconfigure(index=8, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)

label = tk.Label(
    root,
    text="Чтобы опознать из текстового файла нажмите кнопку <open file>",
    font="ansi 12",
).grid(row=0, sticky=tk.NSEW, column=0)

label = tk.Label(
    root,
    text="Или введи текст в ячейку ниже",
    font="ansi 12",
).grid(row=2, sticky=tk.NSEW)


text_editor = tk.Text(height=3)
text_editor.grid(row=3, sticky=tk.NSEW)


def read_text():
    text = text_editor.get("1.0", tk.END)
    text_editor.delete("1.0", tk.END)
    answer.insert(tk.END, f"~~~ {use_model_nb(text)} \n")
    answer.insert(tk.END, f"~~~ {use_model_lr(text)} \n")


def open_file():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        with open(filepath, "r", encoding="utf-8") as file:
            c = 0
            for text in file.read().split("---"):
                c += 1
                answer.insert(tk.END, f"{c}:\n")
                answer.insert(tk.END, f"~~~ {use_model_nb(text)} \n")
                answer.insert(tk.END, f"~~~ {use_model_lr(text)} \n")


read_button = ttk.Button(text="read text", command=read_text)
read_button.grid(row=5, sticky=tk.NSEW, column=0)

file_button = ttk.Button(text="open file", command=open_file)
file_button.grid(row=1, sticky=tk.NSEW, column=0)

answer = tk.Text(height=3)
answer.grid(row=7, sticky=tk.NSEW)

root.mainloop()
