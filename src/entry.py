from tkinter import *
from tkinter import ttk
from typing import ClassVar, Dict, List
from tkinter.filedialog import askdirectory
from os import chdir, listdir
from re import findall
from threading import Thread

root: ClassVar = Tk()
root.geometry("400x700")
root.title("Entry test")
root.configure(background="#fff")

root_theme = ttk.Style()
root_theme.theme_use('clam')
items: List = []
search_list: ClassVar = []


def add_files() -> None:
    global items
    target_dir: str = "C:/Users/Mateusz/Music"
    if bool(target_dir):
        chdir(target_dir)
        for i, file in enumerate(listdir(target_dir)):
            if file.endswith(".mp3"):
                items.append(file)
                list_box.insert(i + 1, file)


def search(e=None) -> None:
    global items, search_list
    if bool(search_box.get()):
        list_box.select_clear(0, END)
        list_box.delete(0, END)
        search_list = []
        for item in items:
            if bool(findall(search_box.get().lower(), item.lower())):
                list_box.insert(len(items), item)
                search_list.append(item)
        if bool(search_list):
            seperator.configure(background='#00E676')
        else:
            seperator.configure(background='#B31412')
    else:
        list_box.select_clear(0, END)
        list_box.delete(0, END)
        for item in items:
            list_box.insert(len(items), item)
        seperator.configure(background='#000')


def list_box_select(e=None) -> None:
    global search_list, items
    if bool(search_box.get()) and bool(search_list):
        print(search_list[list_box.curselection()[0]])
    elif bool(items) and bool(list_box.curselection()):
        print(items[list_box.curselection()[0]])


search_frame: ClassVar = Frame(root)
search_frame.configure(background="#fff")
seperator: ClassVar = Frame(search_frame)
seperator.configure(background="#000")
seperator.place(relx=0.5, rely=0.6, relwidth=0.99, relheight=0.4, anchor='n')
search_box: ClassVar = Entry(search_frame, font=('Bahnschrift', 18), exportselection=1, relief='flat',
                             selectbackground="#000", selectforeground="#fff", )

search_box.place(relx=0.5, rely=0.06, relwidth=0.99, relheight=0.86, anchor='n')

search_frame.place(relx=0.5, rely=0.01, relwidth=0.99, relheight=0.1, anchor='n')

list_box: ClassVar = Listbox(root, font=('Bahnschrift', 11), relief="flat", exportselection=0, cursor="hand2"
                             , bd=0, activestyle="none", takefocus=False, selectmode="SINGLE",
                             highlightthickness=0, selectbackground="#B31412", foreground='#000', background='#fff',)
list_box.place(relx=0.5, rely=0.12, relwidth=0.99, relheight=0.87, anchor='n')

search_box.bind("<KeyRelease>", search)
list_box.bind("<<ListboxSelect>>", list_box_select)
Thread(target=add_files, daemon=True).start()
root.mainloop()
