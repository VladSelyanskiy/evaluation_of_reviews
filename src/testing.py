from usage_of_models import use_model, tokenize_sentence

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Макет")
root.geometry("600x400")

root.grid_rowconfigure(index=0, weight=1)
root.grid_rowconfigure(index=1, weight=1)
root.grid_rowconfigure(index=2, weight=1)
root.grid_rowconfigure(index=4, weight=1)
root.grid_rowconfigure(index=5, weight=1)
root.grid_rowconfigure(index=6, weight=1)
root.grid_rowconfigure(index=7, weight=1)
root.grid_columnconfigure(index=0, weight=1)
root.grid_columnconfigure(index=1, weight=1)

label = tk.Label(
    root,
    text="Чтобы опознать из текстового файла\nНажмите кнопку <выбрать файл>'\n",
    font="ansi 15",
    anchor="nw",
    justify="left",
).grid(row=0, sticky=tk.NSEW, column=0)

label = tk.Label(
    root,
    text="Или введи текст в ячейку ниже\n",
    font="ansi 15",
    anchor="nw",
    justify="left",
).grid(row=2, sticky=tk.NSEW)


text_editor = tk.Text(height=2)
text_editor.grid(row=4, sticky=tk.NSEW)


def read_text():
    text = text_editor.get("1.0", tk.END)
    text_editor.delete("1.0", tk.END)
    answer.insert(tk.END, f"~~~ {use_model(text)} \n")


answer = tk.Text(height=2)
answer.grid(row=7, sticky=tk.NSEW)

next_button = ttk.Button(text="read text", command=read_text)
next_button.grid(row=5, sticky=tk.NSEW, column=0)

root.mainloop()
