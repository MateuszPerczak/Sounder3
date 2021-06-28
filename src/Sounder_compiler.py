try:
    import os
    import sys
    import time
    import threading
    import json
    import shutil
    from tkinter import *
    from tkinter import ttk
    import subprocess
    import zipfile
    import logging
    from typing import ClassVar, Dict, List
except ImportError as error_obj:
    print(error_obj)
    sys.exit(1)

# dir
sounder_dir: str = os.getcwd()
# sounder_dir: str = os.path.dirname(sys.executable)
user_path: str = os.path.expanduser("~")
# main window
main_window: ClassVar = Tk()
main_window.geometry("950x600")
main_window.minsize(600, 500)
main_window.configure(background="#fff")
main_window.title("Sounder3 Builder")
main_window.iconbitmap(sounder_dir + "\\icon.ico")
# style
main_theme: ClassVar = ttk.Style()
main_theme.theme_use('clam')
main_theme.configure("TButton", background='#fff', relief="flat", font=('Bahnschrift', 13), foreground='#000')
main_theme.map("TButton", background=[('pressed', '!disabled', '#fff'), ('active', '#eee')])
main_theme.configure("Vertical.TScrollbar", gripcount=0, relief="flat", background="#fff", darkcolor="#fff"
                     , lightcolor="#fff", troughcolor="#fff", bordercolor="#fff", arrowcolor="#000")
main_theme.map("Vertical.TScrollbar", background=[('pressed', '!disabled', '#eee'), ('active', '#eee')])
# end


def py_builder() -> bool:
    global sounder_dir, user_path
    try:
        os.chdir(sounder_dir)
        push_info("\n\nSounder Builder: The building process has started.")
        command: List = ['pyinstaller', '-w', '-i', 'icon.ico', 'Sounder3.py']
        files_to_copy: List = []
        path_to_dist: str = os.path.join(sounder_dir, "dist\\Sounder3")
        path_to_desktop = os.path.join(user_path, "Desktop")
        config = {"refresh_time": 1.0, "theme": "light", "version": "0.0.0", "transition_duration": 1,
                  "gtr_buffer": False, "mode": "r_n",
                  "last_song": "", "continue": False, "path": user_path + "\\Music", "fade": False, "debug": False,
                  "update": True}
    except Exception as error_obj:
        logging.error(error_obj, exc_info=True)
        push_info("Sounder Builder: Error")
        return False
    try:
        shell: ClassVar = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as grepexc:
        push_info("\n\n" + str(grepexc.output))
        return False
    for line in iter(shell.stdout.readline, b''):
        push_info(str(line.decode("utf-8")))
    shell.wait()
    try:
        if shell.returncode == 0:
            time.sleep(2)
            push_info("\n\nSounder Builder: Preparing for files transfer.")
            if os.path.isdir("__pycache__"):
                push_info("Sounder Builder: Removing __pycache__")
                # shutil.rmtree("__pycache__")
            if os.path.isdir("build"):
                push_info("Sounder Builder: Removing build.")
                # shutil.rmtree("build")
            if os.path.isfile("Sounder3.spec"):
                push_info("Sounder Builder: Removing Sounder3.spec")
                os.remove("Sounder3.spec")
            if os.path.isdir("dist"):
                for file in os.listdir(sounder_dir):
                    if file.endswith(".png") or file.endswith(".ico") or file.endswith(".txt") or file.endswith(".log") or file.endswith(".json") or file == "Updater.exe":
                        files_to_copy.append(file)
                for file in files_to_copy:
                    push_info("Sounder Builder: Copying " + str(file))
                    shutil.copy(file, path_to_dist)
                push_info("Sounder Builder: Preparing packages.")
                push_info("Sounder Builder: Removing config file.")
                os.remove(os.path.join(path_to_dist, "cfg.json"))
                time.sleep(1)
                push_info("Sounder Builder: Preparing zip.")
                os.chdir(path_to_dist)
                with zipfile.ZipFile(os.path.join(path_to_desktop, "package.zip"), 'w') as zip_obj:
                    for file in os.listdir(path_to_dist):
                        if file == "Updater.exe":
                            continue
                        zip_obj.write(file)
                time.sleep(2)
                push_info("Sounder Builder: Preparing cfg.json")
                with open('cfg.json', 'w') as data:
                    json.dump(config, data)
                os.chdir(path_to_desktop)
                push_info("Sounder Builder: Preparing final release.")
                shutil.move(path_to_dist, path_to_desktop)
                os.system(str("copy " + os.path.join(sounder_dir, "dist") + " " + path_to_desktop + "/o/h/e/k/f/c"))
                push_info("Sounder Builder: Cleaning folders.")
                os.chdir(sounder_dir)
                shutil.rmtree("dist")
                push_info("\n\nSounder Builder: Done.")
    except Exception as error_obj:
        logging.error(error_obj, exc_info=True)
        push_info("Sounder Builder: Error")
        return False
    return True


def build() -> None:
    build_thread: ClassVar = threading.Thread(target=py_builder, )
    build_thread.daemon = True
    build_thread.start()


def push_info(info) -> None:
    build_info.configure(state="normal")
    build_info.insert(END, str(info).rstrip() + "\n")
    build_info.see("end")
    build_info.configure(state="disabled")


info_frame: ClassVar = Frame()
build_scroll_bar: ClassVar = ttk.Scrollbar(info_frame, orient=VERTICAL, cursor="hand2", takefocus=False)
build_info: ClassVar = Text(info_frame, selectbackground="#fff", selectforeground="#000", bd=0, cursor="arrow"
                            , takefocus=0, font=('Bahnschrift', 10), yscrollcommand=build_scroll_bar.set)
build_scroll_bar.configure(command=build_info.yview)
build_info.pack(side=LEFT, fill=BOTH, expand=True)
build_scroll_bar.pack(side=LEFT, fill=Y)

info_frame.place(relx=0.5, rely=0.01, relwidth=0.99, relheight=0.9, anchor="n")
build_button: ClassVar = ttk.Button(main_window, text="Build", takefocus=False, cursor="hand2", command=build)
build_button.place(relx=0.5, rely=0.915, relwidth=0.5, anchor="n")

push_info("Welcome to Sounder3 Builder\nVersion 1.0.0\nby Mateusz Perczak")
logging.basicConfig(filename=sounder_dir + "\\errors.log", level=logging.ERROR)

main_window.mainloop()
