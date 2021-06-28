try:
    from os import getcwd, startfile, rename, remove
    from os.path import dirname, isfile, basename
    from threading import Thread
    from json import load
    from tkinter import Tk, PhotoImage, sys, Frame
    from tkinter import ttk
    from typing import ClassVar, Dict, List
    from requests import get
    from zipfile import ZipFile
    import logging
    from io import BytesIO
    from time import sleep
    from psutil import process_iter
    from PIL import Image, ImageSequence, ImageTk
except ImportError as e:
    sys.exit(e)

# dir
sounder_dir: str = getcwd()
# sounder_dir: str = dirname(sys.executable)
# log
logging.basicConfig(filename=f"{sounder_dir}\\errors.log", level=logging.ERROR)
# window setup
updater_window: ClassVar = Tk()
updater_window.withdraw()
updater_window.geometry(f"375x100+{int(updater_window.winfo_x() + ((updater_window.winfo_screenwidth() - 375) / 2))}"
                        f"+{int(updater_window.winfo_y() +((updater_window.winfo_screenheight() - 100) / 2))}")
updater_window.title("Sounder updater")
try:
    updater_window.iconbitmap(f"{sounder_dir}\\icon.ico")
except:
    sys.exit(1)
updater_window.resizable(width=False, height=False)
updater_window.configure(background="#fff")
# theme
updater_theme = ttk.Style()
updater_theme.theme_use('clam')
updater_theme.configure("TLabel", background='#fff', foreground='#000', border='0')
updater_theme.configure("Horizontal.TProgressbar", foreground='#fff', background='#000', lightcolor='#fff'
                        , darkcolor='#fff', bordercolor='#fff', troughcolor='#fff')
updater_theme.configure("TButton", relief="flat", background='#000', font=('Bahnschrift', 10), foreground='#fff')
updater_theme.map("TButton", background=[('pressed', '!disabled', '#000'), ('active', '#111')])
# variables
config: Dict = {}
server_version: str
package = b''

# functions


def dump(err_obj: ClassVar) -> None:
    error_reason_label.configure(text="Error: " + logging.getLevelName(err_obj))
    show(error_frame)
    logging.error(err_obj, exc_info=True)


def show(window) -> bool:
    try:
        window.tkraise()
        return True
    except Exception as e:
        dump(e)
        return False


def load_config() -> bool:
    global config
    if isfile('cfg.json'):
        try:
            with open('cfg.json', 'r') as data:
                config = load(data)
            return True
        except:
            return False
    else:
        return False


def close() -> None:
    for widget in updater_window.winfo_children():
        widget.destroy()
    updater_window.destroy()
    sys.exit(0)


def change_mode(mode: str) -> None:
    try:
        update_progress.stop()
        update_progress["value"] = 0
        update_progress["maximum"] = 100
        if mode == "determinate":
            update_progress.configure(mode="determinate")
        elif mode == "indeterminate":
            update_progress.configure(mode="indeterminate")
            update_progress.start(4)
    except Exception as e:
        dump(e)


def update() -> bool:
    global server_version, package, sounder_dir
    chunk_size: int = 8192
    change_mode("determinate")
    Thread(target=load_img, daemon=True).start()
    show(checking_frame)
    try:
        bytes_downloaded: float = 0
        server_zip = get(f"https://github.com/losek1/Sounder3/releases/download/v{server_version}/package.zip"
                         , stream=True)
        if server_zip.status_code == 200:
            update_progress["maximum"] = int(server_zip.headers.get('Content-Length'))
            show(update_frame)
            for chunk in server_zip.iter_content(chunk_size=chunk_size):
                if chunk:
                    package += chunk
                    bytes_downloaded += chunk_size
                    update_progress["value"] = bytes_downloaded
                    update_data.configure(text=f"{round(bytes_downloaded / 1000000, 1)}MB / {round(int(server_zip.headers.get('Content-Length')) / 1000000, 1)}MB")
            for process in process_iter():
                if process.name() == "Sounder3.exe":
                    process.kill()
            change_mode("indeterminate")
            update_label.configure(text="Installing updates ...")
            with ZipFile(BytesIO(package)) as zip_file:
                for file in zip_file.namelist():
                    update_data.configure(text=f"{zip_file.namelist().index(file)} / {len(zip_file.namelist())}")
                    if file == "Updater.exe" or file == "errors.log":
                        continue
                    try:
                        zip_file.extract(file, sounder_dir)
                    except Exception as error_obj:
                        logging.error(error_obj, exc_info=True)
            show(finish_frame)
            sleep(3)
            open_app()
            close()
        else:
            raise Exception("Cannot contact GitHub servers")
    except Exception as e:
        dump(e)
        return True


def check_updates() -> bool:
    global config, server_version
    try:
        server_version = get(
            "https://raw.githubusercontent.com/losek1/Sounder3/master/updates/version.txt").text.strip()
        if int(config["version"].replace(".", "")) < int(server_version.replace(".", "")):
            return True
        else:
            return False
    except Exception as e:
        dump(e)


def open_app() -> None:
    try:
        if isfile("Sounder3.exe"):
            startfile("Sounder3.exe")
    except Exception as e:
        dump(e)


def update_task() -> None:
    Thread(target=update, daemon=True).start()


def self_upgrade() -> bool:
    try:
        if basename(sys.argv[0]) == "New-Updater.exe":
            if isfile("Updater.exe"):
                remove("Updater.exe")
            rename(sys.argv[0], "Updater.exe")
            return False
        elif isfile("New-Updater.exe"):
            startfile("New-Updater.exe")
            return True
        else:
            return False
    except Exception as e:
        dump(e)


def show_gui() -> None:
    show(checking_frame)
    updater_window.deiconify()
    updater_window.lift()
    updater_window.focus_force()


def init() -> None:
    if self_upgrade():
        close()
    elif load_config():
        show_gui()
        if check_updates():
            update_task()
        else:
            show(choice_frame)


def load_img() -> None:
    try:
        img_frames: List = []
        download_img: ClassVar = Image.open("download_light.gif")
        for frame in ImageSequence.Iterator(download_img):
            img_frames.append(ImageTk.PhotoImage(frame.copy().convert('RGBA').resize((48, 48))))
        if len(img_frames) > 1:
            while True:
                for frame in img_frames:
                    update_img_label.configure(image=frame)
                    sleep(0.02)
        else:
            update_img_label.configure(image=img_frames)
    except Exception as e:
        dump(e)


# frames
# error frame
error_frame: ClassVar = Frame(updater_window)
error_frame.configure(background="#fff")
error_reason_label: ClassVar = ttk.Label(error_frame, text="Error:", anchor='center', font='Bahnschrift 11')
error_exit_button: ClassVar = ttk.Button(error_frame, text="EXIT", cursor="hand2", takefocus=False, command=close)
error_reason_label.place(relx=0.5, rely=0, relheight=0.58, anchor="n")
error_exit_button.place(relx=0.5, rely=0.6, relwidth=0.23, anchor="n")
error_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
# end
# update frame
update_frame: ClassVar = Frame(updater_window)
update_frame.configure(background="#fff")
update_img_label: ClassVar = ttk.Label(update_frame, image=None, anchor='center')
update_label: ClassVar = ttk.Label(update_frame, text="Downloading updates ...", font='Bahnschrift 11')
update_data: ClassVar = ttk.Label(update_frame, text="-- MB / --MB", font='Bahnschrift 10', anchor='center')
update_progress: ClassVar = ttk.Progressbar(update_frame, orient='horizontal')
update_img_label.place(relx=0, rely=0, relwidth=0.25, relheight=1)
update_label.place(relx=0.25, rely=0.15, relwidth=0.45, relheight=0.25)
update_data.place(relx=0.70, rely=0.15, relwidth=0.30, relheight=0.25)
update_progress.place(relx=0.25, rely=0.6, relwidth=0.75, relheight=0.25)
update_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
# end
# check frame
checking_frame: ClassVar = Frame(updater_window)
checking_frame.configure(background="#fff")
checking_label: ClassVar = ttk.Label(checking_frame, text="Verifying\n"
                                                          ". . .", font='Bahnschrift 16', anchor='center', justify='center')
checking_label.place(relx=0.5, rely=0, relheight=1, anchor="n")
checking_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
# end
# choice frame
choice_frame: ClassVar = Frame(updater_window)
choice_frame.configure(background="#fff")
choice_label: ClassVar = ttk.Label(choice_frame, text="The latest version of Sounder is already installed.\n"
                                                      " Would you like to install it anyway?", font='Bahnschrift 11'
                                   , anchor='center', justify='center')
choice_install_button: ClassVar = ttk.Button(choice_frame, text="INSTALL", cursor="hand2", takefocus=False,
                                             command=update_task)
choice_exit_button: ClassVar = ttk.Button(choice_frame, text="EXIT", cursor="hand2", takefocus=False, command=close)
choice_label.place(relx=0.5, rely=0.1, anchor="n")
choice_install_button.place(relx=0.3, rely=0.6, anchor="n")
choice_exit_button.place(relx=0.7, rely=0.6, anchor="n")
choice_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
# end
# finish frame
finish_frame: ClassVar = Frame(updater_window)
finish_frame.configure(background="#fff")
finish_label: ClassVar = ttk.Label(finish_frame, text="All done!\nLaunching sounder in 3s"
                                   , anchor='center', justify='center', font='Bahnschrift 17')
finish_label.place(relx=0, rely=0, relwidth=1, relheight=1)
finish_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
# end
Thread(target=init, daemon=True).start()

updater_window.mainloop()
