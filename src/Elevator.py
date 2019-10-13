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
except ImportError:
    sys.exit(2)

# dir
sounder_dir: str = os.getcwd()
# sounder_dir: str = os.path.dirname(sys.executable)
# end
main_window: ClassVar = Tk()
main_window.geometry("300x150")
main_window.title("Elevator")
main_window.iconbitmap(sounder_dir + "\\icon.ico")
main_window.resizable(width=FALSE, height=FALSE)
main_theme = ttk.Style()
main_theme.theme_use('clam')
config: Dict
words: List = ["I swear it's almost done", "Counting to infinity", "Bending the spoon", "Locating the required gigapixels to render", "Spinning up the hamster", "We're building the buildings as fast as we can", "Keep calm and npm install", "Git happens", "Didn't know paint dried so quickly", "Dividing by zero", "Loading funny message", "Leaking into memory"]
server_version: str


def is_admin():
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
            pass
    return False


def check_for_update() -> bool:
    global config, server_version
    try:
        server_version = requests.get("https://raw.githubusercontent.com/losek1/Sounder3/master/updates/version.txt").text
        if int(config["version"].replace(".", "")) < int(server_version.replace(".", "")):
            return True
        return False
    except:
        return False


def download_package() -> bool:
    global server_version
    try:
        with open("package.zip", 'wb') as file:
            file.write(requests.get("https://github.com/losek1/Sounder3/releases/download/v" + str(server_version) + "/package.zip").content)
        return True
    except:
        return False


def update() -> bool:
    global sounder_dir
    try:
        with zipfile.ZipFile('package.zip', 'r') as zip_ref:
            zip_ref.extractall(sounder_dir)
        os.remove('package.zip')
        update_progress.stop()
    except:
        return False
    return True


def init() -> None:
    if load_config():
        apply_theme()
        if check_for_update():
            if download_package():
                if update():
                    close()


def close():
    if os.path.isfile("Sounder3.exe"):
        os.system("start Sounder3.exe")
    main_window.destroy()
    sys.exit(0)


def apply_theme() -> None:
    global config
    if config["theme"] == "light":
        main_theme.configure("W.TLabel", background='#fff', foreground='#000', border='0')
        main_theme.configure("W.Horizontal.TProgressbar", foreground='#000', background='#000', lightcolor='#fff'
                             , darkcolor='#fff', bordercolor='#fff', troughcolor='#fff')
        main_window.configure(background="#fff")
        update_label.configure(background="#fff", foreground="#000")
        funny_label.configure(background="#fff", foreground="#000")
        info_label.configure(background="#fff", foreground="#000")
    elif config["theme"] == "dark":
        main_theme.configure("W.TLabel", foreground='#fff', background='#000', border='0')
        main_theme.configure("W.Horizontal.TProgressbar", foreground='#000', background='#1e88e5', lightcolor='#000'
                             , darkcolor='#000', bordercolor='#000', troughcolor='#000')
        main_window.configure(background="#000")
        update_label.configure(background="#000", foreground="#fff")
        funny_label.configure(background="#000", foreground="#fff")
        info_label.configure(background="#000", foreground="#fff")


# UI
update_label: ClassVar = ttk.Label(main_window, text="Updating Sounder", font='Bahnschrift 18', anchor="center")
funny_label: ClassVar = ttk.Label(main_window, text=random.SystemRandom().choice(words), font='Bahnschrift 10', anchor="center")
info_label: ClassVar = ttk.Label(main_window, text="This can take a while", font='Bahnschrift 9', anchor="center")
update_progress: ClassVar = ttk.Progressbar(main_window, orient=HORIZONTAL, mode="indeterminate", style="W.Horizontal.TProgressbar")
update_label.place(relx=0, rely=0.02, relwidth=1)
funny_label.place(relx=0, rely=0.3, relwidth=1)
info_label.place(relx=0, rely=0.8, relwidth=1)
update_progress.place(relx=0.5, rely=0.917, relwidth=0.9, height=12, anchor="n")
# end
if is_admin():
    update_progress.start(15)
    init_thread = threading.Thread(target=init, )
    init_thread.daemon = True
    init_thread.start()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
    sys.exit(1)
main_window.protocol("WM_DELETE_WINDOW", close)
main_window.mainloop()
