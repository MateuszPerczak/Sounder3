try:
    import os
    import sys
    import threading
    import json
    from tkinter import *
    from tkinter import ttk
    from typing import ClassVar, Dict, List
    import requests
    import zipfile
    import ctypes
    import logging
    import io
except ImportError:
    sys.exit(1)

# dir
# sounder_dir: str = os.getcwd()
sounder_dir: str = os.path.dirname(sys.executable)
# log
logging.basicConfig(filename=sounder_dir + "\\errors.log", level=logging.ERROR)
# window setup
updater_window: ClassVar = Tk()
updater_window.withdraw()
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
config: Dict
status: ClassVar = StringVar()
task: ClassVar = StringVar()
logo_label: ClassVar
info_progress: ClassVar
info_label: ClassVar
task_label: ClassVar


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


def close() -> None:
    updater_window.destroy()
    sys.exit(0)


def open_sounder():
    try:
        if os.path.isfile("Sounder3.exe"):
            os.startfile("Sounder3.exe")
    except Exception as error_obj:
        logging.error(error_obj, exc_info=True)


def update() -> None:
    status.set("Checking...")
    info_progress.start(4)
    info_progress.configure(mode="indeterminate")
    downloaded_zip: bytes = b''
    bytes_downloaded: float = 0
    file_size: float
    try:
        server_version = requests.get(
            "https://raw.githubusercontent.com/losek1/Sounder3/master/updates/version.txt").text.strip()
        if int(config["version"].replace(".", "")) < int(server_version.replace(".", "")):
            info_progress.stop()
            try:
                info_progress.configure(mode="determinate")
                server_zip = requests.get(
                    "https://github.com/losek1/Sounder3/releases/download/v" + str(server_version) + "/package.zip",
                    stream=True)
                if server_zip.status_code == 200:
                    file_size = round(int(server_zip.headers.get('Content-Length')) / 1000000, 1)
                    info_progress["maximum"] = int(server_zip.headers.get('Content-Length'))
                    status.set("Downloading...")
                    for chunk in server_zip.iter_content(chunk_size=8192):
                        if chunk:
                            downloaded_zip += chunk
                            bytes_downloaded += 8192
                            info_progress["value"] = bytes_downloaded
                            task.set(str(round(bytes_downloaded / 1000000, 1)) + "MB / " + str(file_size) + "MB")
                    info_progress.stop()
                    info_progress["maximum"] = 100
                    info_progress["value"] = 0
                    try:
                        task.set("")
                        status.set("Installing...")
                        info_progress.configure(mode="indeterminate")
                        info_progress.start(4)
                        with zipfile.ZipFile(io.BytesIO(downloaded_zip)) as zip_file:
                            for file in zip_file.namelist():
                                if file == "Updater.exe":
                                    continue
                                task.set("Replacing:" + file)
                                try:
                                    zip_file.extract(file, sounder_dir)
                                except Exception as error_obj:
                                    logging.error(error_obj, exc_info=True)
                                    task.set("Skipping:" + file)
                        info_progress.stop()
                        info_progress.configure(mode="determinate")
                        info_progress["maximum"] = 100
                        info_progress["value"] = 0
                        status.set("Done")
                    except Exception as error_obj:
                        logging.error(error_obj, exc_info=True)
                        info_progress.stop()
                        info_progress.configure(mode="determinate")
                        info_progress["maximum"] = 100
                        info_progress["value"] = 0
                        status.set("Failed to extract content!")
                else:
                    info_progress.stop()
                    info_progress.configure(mode="determinate")
                    info_progress["maximum"] = 100
                    info_progress["value"] = 0
                    status.set("Failed to download updates!")
            except Exception as error_obj:
                info_progress.stop()
                info_progress.configure(mode="determinate")
                info_progress["maximum"] = 100
                info_progress["value"] = 0
                status.set("An error occurred while updating!")
                logging.error(error_obj, exc_info=True)
        else:
            info_progress.stop()
            info_progress.configure(mode="determinate")
            info_progress["maximum"] = 100
            info_progress["value"] = 0
            status.set("No updates")
    except Exception as error_obj:
        logging.error(error_obj, exc_info=True)
    info_progress.stop()
    info_progress.configure(mode="determinate")


def gui_setup() -> None:
    global logo_label, info_progress, info_label, task_label
    logo_label = ttk.Label(updater_window, image=sounder_logo, background="#fff")
    info_progress = ttk.Progressbar(updater_window, orient=HORIZONTAL, style="W.Horizontal.TProgressbar")
    info_label = ttk.Label(updater_window, textvariable=status, background="#fff", foreground="#000",
                           font='Bahnschrift 14', anchor="center")
    task_label = ttk.Label(updater_window, textvariable=task, background="#fff", foreground="#000",
                           font='Bahnschrift 10', anchor="center", border='0')
    logo_label.place(relx=0.5, rely=0.1, anchor="n")
    info_progress.place(relx=0.5, rely=0.6, relwidth=0.99, height=15, anchor="n")
    task_label.place(relx=0, rely=0.67, relwidth=0.98)
    info_label.place(relx=0, rely=0.8, relwidth=1)
    updater_window.deiconify()


def main() -> None:
    if is_admin():
        gui_setup()
        if load_config():
            update()
            open_sounder()
            close()
        else:
            status.set("Config file not found")
    else:
        close()


main_thread = threading.Thread(target=main, )
main_thread.daemon = True
main_thread.start()
updater_window.protocol("WM_DELETE_WINDOW", close)
updater_window.mainloop()