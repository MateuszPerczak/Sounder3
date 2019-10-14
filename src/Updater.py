try:
    import os
    import threading
    import json
    from tkinter import *
    from tkinter import ttk
    from typing import ClassVar, Dict, List
    import requests
    import zipfile
    import random
    import ctypes
    import time
except ImportError:
    sys.exit(1)

# dir
# sounder_dir: str = os.getcwd()
sounder_dir: str = os.path.dirname(sys.executable)
# window setup
updater_window: ClassVar = Tk()
updater_window.geometry("350x200")
updater_window.title("Sounder updater")
updater_window.iconbitmap(sounder_dir + "\\icon.ico")
updater_window.resizable(width=FALSE, height=FALSE)
updater_window.configure(background="#fff")
# images
sounder_logo = PhotoImage(file="logo_1.png")
# theme
updater_theme = ttk.Style()
updater_theme.theme_use('clam')
updater_theme.configure("W.TLabel", background='#fff', foreground='#000', border='0')
updater_theme.configure("W.Horizontal.TProgressbar", foreground='#000', background='#000', lightcolor='#fff'
                        , darkcolor='#fff', bordercolor='#fff', troughcolor='#fff')
# variables
server_version: str
config: Dict
status: ClassVar = StringVar()
size: ClassVar = StringVar()
# functions


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def load_config() -> bool:
    global config
    if os.path.isfile('cfg.json'):
        try:
            with open('cfg.json', 'r') as data:
                config = json.load(data)
            return True
        except:
            return False
    else:
        return False


def check_for_update() -> bool:
    global config, server_version
    try:
        server_version = requests.get(
            "https://raw.githubusercontent.com/losek1/Sounder3/master/updates/version.txt").text.strip()
        if int(config["version"].replace(".", "")) < int(server_version.replace(".", "")):
            return True
        else:
            return False
    except:
        return False


def download_update() -> bool:
    global server_version, sounder_dir
    try:
        server_zip = requests.get("https://github.com/losek1/Sounder3/releases/download/v" + str(server_version) + "/package.zip", stream=True)
        file_size: float = round(int(server_zip.headers.get('Content-Length')) / 1000000, 1)
        bytes_downloaded: float = 0
        info_progress["maximum"] = int(server_zip.headers.get('Content-Length'))
        status.set("Downloading...")
        with open('package.zip', 'wb') as file:
            for chunk in server_zip.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    bytes_downloaded += 8192
                    info_progress["value"] = bytes_downloaded
                    size.set(str(round(bytes_downloaded / 1000000, 1)) + "MB / " + str(file_size) + "MB")
        try:
            size.set("")
            status.set("Installing...")
            info_progress.configure(mode="indeterminate")
            info_progress.start()
            with zipfile.ZipFile('package.zip', 'r') as zip_file:
                zip_file.extractall(sounder_dir)
            os.remove('package.zip')
            close()
        except:
            status.set("An error occurred while updating!")
            return False
        return True
    except:
        status.set("An error occurred while updating!")
        return False


def close():
    if os.path.isfile("Sounder3.exe"):
        os.system("start Sounder3.exe")
    updater_window.destroy()
    sys.exit(0)


def main() -> None:
    if is_admin():
        if load_config():
            status.set("Checking...")
            info_progress.start(4)
            if check_for_update():
                info_progress.stop()
                info_progress.configure(mode="determinate")
                if download_update():
                    status.set("Done")
            else:
                info_progress.stop()
                status.set("No updates!")
        else:
            info_progress.stop()
            status.set("Missing files!")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
        updater_window.destroy()
        sys.exit(0)


logo_label: ClassVar = ttk.Label(updater_window, image=sounder_logo, background="#fff")
info_progress: ClassVar = ttk.Progressbar(updater_window, orient=HORIZONTAL, mode="indeterminate",
                                          style="W.Horizontal.TProgressbar")
info_label: ClassVar = ttk.Label(updater_window, textvariable=status, background="#fff", foreground="#000",
                                 font='Bahnschrift 14', anchor="center")
size_label: ClassVar = ttk.Label(updater_window, textvariable=size, background="#fff", foreground="#000",
                                 font='Bahnschrift 10', anchor="center", border='0')
logo_label.place(relx=0.5, rely=0.1, anchor="n")
info_progress.place(relx=0.5, rely=0.6, relwidth=0.99, height=15, anchor="n")
size_label.place(relx=0, rely=0.67, relwidth=0.98)
info_label.place(relx=0, rely=0.8, relwidth=1)
main_thread = threading.Thread(target=main, )
main_thread.daemon = True
main_thread.start()
updater_window.protocol("WM_DELETE_WINDOW", close)
updater_window.mainloop()
