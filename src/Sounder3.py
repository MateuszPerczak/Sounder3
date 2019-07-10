import os
import time
import threading
import json
from pygame import mixer
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from PIL import ImageTk
from PIL import Image
from io import BytesIO
from mutagen.id3 import ID3
from typing import ClassVar, Dict, List

# dir
# sounder_dir: str = os.getcwd()
sounder_dir: str = os.path.dirname(sys.executable)
user_path: str = os.path.expanduser("~")
# end
main_window: ClassVar = Tk()
main_window.geometry("800x500")
main_window.title("Sounder3")
main_window.iconbitmap(sounder_dir + "\\icon.ico")
main_window.resizable(width=FALSE, height=FALSE)
# icons
logo_1_img: ClassVar = PhotoImage(file=sounder_dir + "\\logo_1.png")
error_img: ClassVar = PhotoImage(file=sounder_dir + "\\error_light.png")
# end
# var
path: ClassVar = StringVar()
music_title: ClassVar = StringVar()
music_time: ClassVar = StringVar()
album_name: ClassVar = StringVar()
error_reason: ClassVar = StringVar()
config: Dict = {}
version: str = "3.0.2"
num_of_songs: int = 0
songs: List = []
current_song: int = 0
songs_exists: bool = False
play_button_state: bool = False
mode: str = "r_n"
err: int = 0
default_album_img: ClassVar
repeat_all_img: ClassVar
repeat_one_img: ClassVar
repeat_none_img: ClassVar
forward_img: ClassVar
play_img: ClassVar
pause_img: ClassVar
previous_img: ClassVar
settings_img: ClassVar
back_img: ClassVar
folder_img: ClassVar
refresh_img: ClassVar
toggle_on_img: ClassVar
toggle_off_img: ClassVar
album_img: ClassVar
logo_2_img: ClassVar


# end
# functions


def dump(value: str, cfg: Dict) -> None:
    global sounder_dir
    try:
        os.chdir(sounder_dir)
        with open('errors.log', 'a') as data:
            data.write(value + "\n")
            data.write("Settings dump: \n" + str(cfg) + '\n')
            data.write("You can report a problem on " + "\"https://github.com/losek1/Sounder3/issues\" \n")
    except:
        pass
    if bool(config["path"]):
        os.chdir(config["path"])
    error_reason.set(value)
    show(main_error_frame, "main_error_frame")


def load_settings() -> bool:
    global config, version
    if os.path.isfile('cfg.json'):
        try:
            with open('cfg.json', 'r') as data:
                config = json.load(data)
            return True
        except Exception as e:
            dump(str(e), config)
            return False
    elif not os.path.isfile('cfg.json'):
        config = {"refresh_time": 1.0, "theme": "light", "version": version, "transition_duration": 1,
                  "gtr_buffer": False,
                  "last_song": "", "continue": False, "path": user_path + "\\Music"}
        try:
            with open('cfg.json', 'w') as data:
                json.dump(config, data)
        except Exception as e:
            dump(str(e), config)
            return False
        return True


def save_settings() -> bool:
    global config, sounder_dir
    os.chdir(sounder_dir)
    if os.path.isfile('cfg.json'):
        try:
            with open('cfg.json', 'w') as data:
                json.dump(config, data)
            os.chdir(config["path"])
            return True
        except Exception as e:
            dump(str(e), config)
            return False


def load_music() -> bool:
    global config, num_of_songs, songs
    num_of_songs = -1
    songs = []
    try:
        os.chdir(config["path"])
        for file in os.listdir(config["path"]):
            if file.endswith(".mp3"):
                num_of_songs += 1
                songs.append(file)
    except:
        return False
    return True


def change_dir() -> bool:
    global config
    target_dir: str = askdirectory()
    if bool(target_dir):
        config["path"] = target_dir.rstrip('\n')
        return True
    else:
        return False


def refresh_window() -> None:
    global config, songs, current_song
    path.set(str(config["path"].rstrip('\n')))
    left_player_music_list.delete(0, END)
    if bool(songs):
        for element in songs:
            element: str = element.rstrip('.mp3')
            left_player_music_list.insert(len(songs), element)
        left_player_music_list.select_set(current_song)


def start_music() -> None:
    global config, songs, current_song
    if config["last_song"] and config["continue"] and bool(songs):
        try:
            current_song = songs.index(config["last_song"])
            music("play")
        except:
            config["last_song"] = ""


def refresh_dir() -> None:
    if load_music():
        refresh_window()


def verify_settings() -> None:
    global config
    try:
        if not type(config["refresh_time"]) is float:
            config["refresh_time"] = 1.0
    except:
        config["refresh_time"] = 1.0
    try:
        if not type(config["theme"]) is str:
            config["theme"] = "light"
    except:
        config["theme"] = "light"
    try:
        if not type(config["version"]) is str:
            config["version"] = version
    except:
        config["version"] = version
    try:
        if not type(config["transition_duration"]) is int:
            config["transition_duration"] = 1
    except:
        config["transition_duration"] = 1
    try:
        if not type(config["gtr_buffer"]) is bool:
            config["gtr_buffer"] = False
    except:
        config["gtr_buffer"] = False
    try:
        if not type(config["last_song"]) is str:
            config["last_song"] = ""
    except:
        config["last_song"] = ""
    try:
        if not type(config["continue"]) is bool:
            config["continue"] = False
    except:
        config["continue"] = False


def apply_theme() -> bool:
    global config, repeat_all_img, repeat_one_img, repeat_none_img, forward_img, play_img, previous_img, pause_img \
        , toggle_off_img, toggle_on_img, default_album_img, settings_img, back_img, folder_img, refresh_img \
        , play_button_state, mode
    main_theme = ttk.Style()
    main_theme.theme_use('clam')
    try:
        if config["theme"] == "light":
            main_theme.configure("G.Horizontal.TProgressbar", foreground='#000', background='#000', lightcolor='#000',
                                 darkcolor='#fff',
                                 bordercolor='#fff', troughcolor='#fff')
            main_theme.configure("W.TLabel", background='#fff', foreground='#000', border='0')
            main_theme.configure("TButton", background='#fff', relief="flat", font=('Bahnschrift', 11)
                                 , foreground='#000')
            main_theme.map("TButton", background=[('pressed', '!disabled', '#fff'), ('active', '#eee')])
            main_theme.map("TScale", background=[('pressed', '!disabled', '#111'), ('active', '#111')])
            main_theme.configure("TScale", troughcolor='#eee', background='#000', relief="flat", gripcount=0
                                 , darkcolor="#000", lightcolor="#000", bordercolor="#fff")
            main_theme.configure("W.TEntry", foreground='#000', bordercolor='#000', lightcolor='#000',
                                 fieldbackground='#fff',
                                 selectbackground='#000', selectforeground='#fff')
            main_theme.configure("Horizontal.TScrollbar", gripcount=0, relief="flat",
                                 background="#fff", darkcolor="#fff", lightcolor="#fff",
                                 troughcolor="#fff", bordercolor="#fff", arrowcolor="#000")
            main_theme.map("Horizontal.TScrollbar", background=[('pressed', '!disabled', '#eee'), ('active', '#eee')])
            left_player_music_list.configure(selectbackground="#000", foreground='#000', background='#fff'
                                             , relief="flat")
            buttons_player_frame.configure(background="#fff")
            right_player_frame.configure(background="#fff")
            left_player_frame.configure(background="#fff")
            bottom_player_frame.configure(background="#fff")
            top_player_frame.configure(background="#fff")
            left_settings_frame_third.configure(background="#fff")
            left_settings_frame_second.configure(background="#fff")
            left_settings_frame_first.configure(background="#fff")
            left_settings_frame.configure(background="#fff")
            center_settings_frame.configure(background="#fff")
            top_settings_frame.configure(background="#fff")
            main_settings_frame.configure(background="#fff")
            mode_player_frame.configure(background="#fff")
            left_settings_frame_fourth.configure(background="#fff")
            left_player_scrollbar_frame.configure(background="#fff")
            left_player_list_box_frame.configure(background="#fff")
            main_window.configure(background="#fff")
            left_settings_frame_fifth.configure(background="#fff")
            default_album_img = ImageTk.PhotoImage(Image.open(sounder_dir + "\\cover_art_light.png").resize((220, 220)))
            repeat_all_img = PhotoImage(file=sounder_dir + "\\repeat_all_light.png")
            repeat_one_img = PhotoImage(file=sounder_dir + "\\repeat_one_light.png")
            repeat_none_img = PhotoImage(file=sounder_dir + "\\repeat_none_light.png")
            forward_img = PhotoImage(file=sounder_dir + "\\forward_light.png")
            play_img = PhotoImage(file=sounder_dir + "\\play_light.png")
            pause_img = PhotoImage(file=sounder_dir + "\\pause_light.png")
            previous_img = PhotoImage(file=sounder_dir + "\\previous_light.png")
            settings_img = PhotoImage(file=sounder_dir + "\\settings_light.png")
            back_img = PhotoImage(file=sounder_dir + "\\back_light.png")
            folder_img = PhotoImage(file=sounder_dir + "\\file_directory_light.png")
            refresh_img = PhotoImage(file=sounder_dir + "\\refresh_light.png")
            toggle_on_img = PhotoImage(file=sounder_dir + "\\toggle_on_light.png")
            toggle_off_img = PhotoImage(file=sounder_dir + "\\toggle_off_light.png")
            right_player_album_art_label.configure(image=default_album_img)
            mode_player_mode_button.configure(image=repeat_none_img)
            buttons_player_forward_button.configure(image=forward_img)
            if play_button_state:
                buttons_player_play_button.configure(image=pause_img)
            else:
                buttons_player_play_button.configure(image=play_img)
            buttons_player_previous_button.configure(image=previous_img)
            top_player_settings_button.configure(image=settings_img)
            top_settings_back_button.configure(image=back_img)
            top_player_folder_button.configure(image=folder_img)
            top_player_refresh_button.configure(image=refresh_img)
            left_settings_theme_button.configure(image=toggle_off_img)
            if config["gtr_buffer"]:
                left_settings_buffer_button.configure(image=toggle_on_img)
            else:
                left_settings_buffer_button.configure(image=toggle_off_img)
            if mode == "r_n":
                mode_player_mode_button.configure(image=repeat_none_img)
            elif mode == "r_a":
                mode_player_mode_button.configure(image=repeat_all_img)
            elif mode == "r_o":
                mode_player_mode_button.configure(image=repeat_one_img)
            if config["continue"]:
                left_settings_continue_button.configure(image=toggle_on_img)
            else:
                left_settings_continue_button.configure(image=toggle_off_img)
        elif config["theme"] == "dark":
            main_theme.configure("G.Horizontal.TProgressbar", foreground='#1e88e5', background='#1e88e5',
                                 lightcolor='#1e88e5',
                                 darkcolor='#1e88e5', bordercolor='#000', troughcolor='#000')
            main_theme.configure("W.TLabel", foreground='#fff', background='#000', border='0')
            main_theme.configure("TButton", relief="flat", background='#000', font=('Bahnschrift', 11)
                                 , foreground='#fff')
            main_theme.map("TButton", background=[('pressed', '!disabled', '#000'), ('active', '#111')])
            main_theme.map("TScale", background=[('pressed', '!disabled', '#0d77d4'), ('active', '#0d77d4')])
            main_theme.configure("TScale", troughcolor='#111', background='#1e88e5', relief="flat", gripcount=0
                                 , darkcolor="#1e88e5", lightcolor="#1e88e5", bordercolor="#000")
            main_theme.configure("Horizontal.TScrollbar", gripcount=0, relief="flat", background="#000"
                                 , darkcolor="#000", lightcolor="#000", troughcolor="#000", bordercolor="#000"
                                 , arrowcolor="#1e88e5")
            main_theme.map("Horizontal.TScrollbar", background=[('pressed', '!disabled', '#111'), ('active', '#111')])
            left_player_music_list.configure(selectbackground="#1e88e5", foreground='#fff', background='#000'
                                             , relief="flat")
            buttons_player_frame.configure(background="#000")
            right_player_frame.configure(background="#000")
            left_player_frame.configure(background="#000")
            bottom_player_frame.configure(background="#000")
            top_player_frame.configure(background="#000")
            left_settings_frame_third.configure(background="#000")
            left_settings_frame_second.configure(background="#000")
            left_settings_frame_first.configure(background="#000")
            left_settings_frame.configure(background="#000")
            center_settings_frame.configure(background="#000")
            top_settings_frame.configure(background="#000")
            main_settings_frame.configure(background="#000")
            mode_player_frame.configure(background="#000")
            left_settings_frame_fourth.configure(background="#000")
            left_player_scrollbar_frame.configure(background="#000")
            left_player_list_box_frame.configure(background="#000")
            main_window.configure(background="#000")
            left_settings_frame_fifth.configure(background="#000")
            default_album_img = ImageTk.PhotoImage(Image.open(sounder_dir + "\\cover_art_dark.png").resize((220, 220)))
            repeat_all_img = PhotoImage(file=sounder_dir + "\\repeat_all_dark.png")
            repeat_one_img = PhotoImage(file=sounder_dir + "\\repeat_one_dark.png")
            repeat_none_img = PhotoImage(file=sounder_dir + "\\repeat_none_dark.png")
            forward_img = PhotoImage(file=sounder_dir + "\\forward_dark.png")
            play_img = PhotoImage(file=sounder_dir + "\\play_dark.png")
            pause_img = PhotoImage(file=sounder_dir + "\\pause_dark.png")
            previous_img = PhotoImage(file=sounder_dir + "\\previous_dark.png")
            settings_img = PhotoImage(file=sounder_dir + "\\settings_dark.png")
            back_img = PhotoImage(file=sounder_dir + "\\back_dark.png")
            folder_img = PhotoImage(file=sounder_dir + "\\file_directory_dark.png")
            refresh_img = PhotoImage(file=sounder_dir + "\\refresh_dark.png")
            toggle_on_img = PhotoImage(file=sounder_dir + "\\toggle_on_dark.png")
            toggle_off_img = PhotoImage(file=sounder_dir + "\\toggle_off_dark.png")
            right_player_album_art_label.configure(image=default_album_img)
            mode_player_mode_button.configure(image=repeat_none_img)
            buttons_player_forward_button.configure(image=forward_img)
            if play_button_state:
                buttons_player_play_button.configure(image=pause_img)
            else:
                buttons_player_play_button.configure(image=play_img)
            buttons_player_previous_button.configure(image=previous_img)
            top_player_settings_button.configure(image=settings_img)
            top_settings_back_button.configure(image=back_img)
            top_player_folder_button.configure(image=folder_img)
            top_player_refresh_button.configure(image=refresh_img)
            left_settings_theme_button.configure(image=toggle_on_img)
            if config["gtr_buffer"]:
                left_settings_buffer_button.configure(image=toggle_on_img)
            else:
                left_settings_buffer_button.configure(image=toggle_off_img)
            if mode == "r_n":
                mode_player_mode_button.configure(image=repeat_none_img)
            elif mode == "r_a":
                mode_player_mode_button.configure(image=repeat_all_img)
            elif mode == "r_o":
                mode_player_mode_button.configure(image=repeat_one_img)

            if config["continue"]:
                left_settings_continue_button.configure(image=toggle_on_img)
            else:
                left_settings_continue_button.configure(image=toggle_off_img)
        else:
            dump("Failed to apply theme", config)
            config["theme"] = "light"
            return False
        return True
    except Exception as e:
        dump(str(e), config)
        return False


def apply_settings() -> bool:
    global config
    try:
        left_settings_refresh_scale.set(config["refresh_time"])
        left_settings_duration_scale.set(config["transition_duration"])
        music_time.set("--:--")
        music_title.set("----------------------")
    except Exception as e:
        dump(str(e), config)
        return False
    return True


def init_mixer() -> bool:
    global config
    try:
        if config["gtr_buffer"]:
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=8192)
        else:
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
        mixer.init()
    except Exception as e:
        dump(str(e), config)
        return False
    try:
        status_thread = threading.Thread(target=song_stats, )
        status_thread.daemon = True
        status_thread.start()
    except Exception as e:
        dump(str(e), config)
        return False
    return True


def init_player() -> None:
    global config
    try:
        if load_settings():
            verify_settings()
            if apply_settings():
                if apply_theme():
                    if init_mixer():
                        if not load_music():
                            while not change_dir():
                                pass
                        load_music()
                        start_music()
                        refresh_window()
                        set_song_attrib()
                        show(main_player_frame, "main_player_frame")
    except Exception as e:
        dump(str(e), config)


def music(button) -> None:
    global num_of_songs, songs, current_song, play_button_state
    print(current_song)
    print(num_of_songs)
    try:
        if button == "forward" and bool(songs):
            if not current_song >= num_of_songs:
                current_song += 1
                if mixer.music.get_busy():
                    mixer.music.stop()
                mixer.music.load(songs[current_song])
                mixer.music.play()
                if not play_button_state:
                    play_button_state = True
                    buttons_player_play_button.configure(image=pause_img)
                set_song_attrib()
        elif button == "play" and bool(songs):
            if not play_button_state:
                if not mixer.music.get_busy():
                    mixer.music.load(songs[current_song])
                    mixer.music.play()
                    set_song_attrib()
                else:
                    mixer.music.unpause()
                play_button_state = True
                buttons_player_play_button.configure(image=pause_img)
            elif play_button_state:
                mixer.music.pause()
                play_button_state = False
                buttons_player_play_button.configure(image=play_img)
        elif button == "play" and not bool(songs):
            if play_button_state:
                mixer.music.stop()
                play_button_state = False
                buttons_player_play_button.configure(image=play_img)
        elif button == "previous" and bool(songs):
            if not current_song <= 0:
                current_song -= 1
                if mixer.music.get_busy():
                    mixer.music.stop()
                mixer.music.load(songs[current_song])
                mixer.music.play()
                if not play_button_state:
                    play_button_state = True
                    buttons_player_play_button.configure(image=pause_img)
                set_song_attrib()
        elif button == "list" and bool(songs):
            if play_button_state:
                if mixer.music.get_busy():
                    mixer.music.stop()
            elif not play_button_state:
                play_button_state = True
                buttons_player_play_button.configure(image=pause_img)
            current_song = left_player_music_list.curselection()[0]
            mixer.music.load(songs[current_song])
            mixer.music.play()
            set_song_attrib()
    except:
        refresh_window()


def set_song_attrib() -> None:
    global songs, current_song, album_img, config
    if bool(songs):
        try:
            tags: ClassVar = ID3(songs[current_song])
            try:
                album: str = tags["TALB"]
                album_name.set(album)
            except:
                album_name.set("")
            try:
                pict: bytes = tags.get("APIC:").data
                album_img = ImageTk.PhotoImage(Image.open(BytesIO(pict)).resize((220, 220)))
                right_player_album_art_label.configure(image=album_img)
            except:
                right_player_album_art_label.configure(image=default_album_img)
            try:
                music_title.set(str(tags["TIT2"]))
            except:
                music_title.set(songs[current_song].rstrip(".mp3"))
        except:
            right_player_album_art_label.configure(image=default_album_img)
            music_title.set(songs[current_song].rstrip(".mp3"))
        left_player_music_list.selection_clear(0, END)
        left_player_music_list.select_set(current_song)
        music_time.set("0:00")
        config["last_song"] = songs[current_song]


def song_stats() -> None:
    global play_button_state, config
    try:
        end = False
        wait = False
        while True:
            if mixer.music.get_busy():
                # time smoothing
                if play_button_state and wait:
                    time.sleep(0.2)
                    wait = False
                elif play_button_state and not wait:
                    song_length = mixer.music.get_pos() / 1000
                    time_minutes, time_seconds = divmod(song_length, 60)
                    music_time.set(str(int(time_minutes)) + ":" + str(int(time_seconds)).zfill(2))
                elif not play_button_state and not wait:
                    wait = True
                # end
                if not end:
                    end = True
                time.sleep(float(config["refresh_time"] * 0.2))
            elif not mixer.music.get_busy():
                if end:
                    play_button_state = False
                    buttons_player_play_button.configure(image=play_img)
                    end = False
                    if config["transition_duration"] != 0:
                        time.sleep(config["transition_duration"])
                    if not mixer.music.get_busy():
                        play_loop()
                time.sleep(float(config["refresh_time"] * 0.5))
    except Exception as e:
        dump(str(e), config)


def play_loop() -> None:
    global mode, current_song, num_of_songs
    if mode == "r_n":
        music("forward")
    elif mode == "r_o":
        music("play")
    elif mode == "r_a":
        if current_song < num_of_songs:
            music("forward")
        else:
            current_song = 0
            music("play")


def mode_change() -> None:
    global mode
    if mode == "r_n":
        mode = "r_a"
        mode_player_mode_button.configure(image=repeat_all_img)
    elif mode == "r_a":
        mode = "r_o"
        mode_player_mode_button.configure(image=repeat_one_img)
    elif mode == "r_o":
        mode = "r_n"
        mode_player_mode_button.configure(image=repeat_none_img)


def show(window, scene) -> bool:
    if scene == "main_settings_frame":
        main_window.title("Sounder3 > settings")
    elif scene == "main_error_frame":
        main_window.title("Sounder3 Error")
    else:
        main_window.title("Sounder3")
    try:
        window.tkraise()
        return True
    except Exception as e:
        dump(str(e), config)
        return False


def close() -> None:
    save_settings()
    main_player_frame.destroy()
    sys.exit()


def change_dir_btn() -> None:
    if change_dir():
        refresh_dir()


def list_box_selector(event=None) -> None:
    music("list")


def set_refresh(value) -> None:
    global config
    config["refresh_time"] = round(float(value), 1)


def set_duration(value) -> None:
    global config
    config["transition_duration"] = round(float(value), 0)


def toggle_theme() -> None:
    global config
    if config["theme"] == "light":
        config["theme"] = "dark"
    elif config["theme"] == "dark":
        config["theme"] = "light"
    if apply_theme():
        set_song_attrib()


def toggle_buffer() -> None:
    global config
    if config["gtr_buffer"]:
        left_settings_buffer_button.configure(image=toggle_off_img)
        config["gtr_buffer"] = False
    else:
        left_settings_buffer_button.configure(image=toggle_on_img)
        config["gtr_buffer"] = True


def toggle_continue() -> None:
    global config
    if config["continue"]:
        left_settings_continue_button.configure(image=toggle_off_img)
        config["continue"] = False
    else:
        left_settings_continue_button.configure(image=toggle_on_img)
        config["continue"] = True


# end
# main init frame
main_init_frame: ClassVar = Frame(main_window, width=800, height=500)
main_init_frame.configure(background="#fff")
main_init_frame.place(x=0, y=0, width=800, height=500)
logo_frame: ClassVar = Frame(main_init_frame)
logo_frame.configure(background="#fff")
logo_label: ClassVar = ttk.Label(logo_frame, image=logo_1_img, font='Bahnschrift 11', background='#fff'
                                 , foreground='#000', border='0')
version_label: ClassVar = ttk.Label(logo_frame, text="V" + version[0], font='Bahnschrift 11', background='#fff'
                                    , foreground='#000', border='0')
logo_label.pack()
version_label.pack()
logo_frame.pack(pady=(170, 0))
# end
# main error frame
main_error_frame: ClassVar = Frame(main_window, width=800, height=500)
main_error_frame.configure(background="#fff")
error_img_label: ClassVar = ttk.Label(main_error_frame, image=error_img, background='#fff', foreground='#000',
                                      border='0')
error_label = ttk.Label(main_error_frame, textvariable=error_reason, background='#fff', foreground='#000', border='0',
                        font='Bahnschrift 13', wraplength=700)
error_img_label.pack(pady=(170, 0))
error_label.pack(pady=(20, 0))
main_error_frame.place(x=0, y=0, width=800, height=500)
# end
# settings frame
main_settings_frame: ClassVar = Frame(main_window)
main_settings_frame.grid(row=0, column=0, sticky='news')
# end
# top settings frame
top_settings_frame: ClassVar = Frame(main_settings_frame)
top_settings_title_label: ClassVar = ttk.Label(top_settings_frame, text="Settings", font='Bahnschrift 15',
                                               style="W.TLabel")
top_settings_back_button: ClassVar = ttk.Button(top_settings_frame, cursor="hand2", takefocus=False,
                                                command=lambda: show(main_player_frame, "main_player_frame"))
top_settings_title_label.pack(side=LEFT, padx=(6, 0))
top_settings_back_button.pack(side=LEFT, padx=(680, 0))
top_settings_frame.pack(fill=X)
# end
# center settings frame
center_settings_frame: ClassVar = Frame(main_settings_frame)
center_settings_separator: ClassVar = ttk.Separator(center_settings_frame, orient="horizontal")
center_settings_separator.pack(fill=X)
center_settings_frame.pack(anchor=N, fill=BOTH)
# end
# left settings frame
left_settings_frame: ClassVar = Frame(center_settings_frame)
left_settings_frame.pack(side=LEFT, anchor=N)
# end
# first setting
left_settings_frame_first: ClassVar = Frame(left_settings_frame)
left_settings_refresh_label: ClassVar = ttk.Label(left_settings_frame_first, text="Refresh rate", font='Bahnschrift 12',
                                                  style="W.TLabel")
left_settings_refresh_scale: ClassVar = ttk.Scale(left_settings_frame_first, from_=1, to=10, orient=HORIZONTAL,
                                                  cursor="hand2",
                                                  command=set_refresh)
left_settings_refresh_label.pack(side=LEFT, padx=(6, 0), pady=(8, 0))
left_settings_refresh_scale.pack(side=RIGHT, padx=(8, 0), pady=(8, 0))
left_settings_frame_first.pack(anchor=W, fill=X)
# end
# second setting
left_settings_frame_second: ClassVar = Frame(left_settings_frame)

left_settings_duration_label: ClassVar = ttk.Label(left_settings_frame_second, text="Transition duration",
                                                   font='Bahnschrift 12',
                                                   style="W.TLabel")
left_settings_duration_scale: ClassVar = ttk.Scale(left_settings_frame_second, from_=0, to=10, orient=HORIZONTAL,
                                                   cursor="hand2",
                                                   command=set_duration)
left_settings_duration_label.pack(side=LEFT, padx=(6, 0), pady=(8, 0))
left_settings_duration_scale.pack(side=RIGHT, padx=(8, 0), pady=(8, 0))
left_settings_frame_second.pack(anchor=W, fill=X)
# end
# third setting
left_settings_frame_third: ClassVar = Frame(left_settings_frame)
left_settings_theme_label: ClassVar = ttk.Label(left_settings_frame_third, text="Dark theme", font='Bahnschrift 11'
                                                , style="W.TLabel")
left_settings_theme_button: ClassVar = ttk.Button(left_settings_frame_third, cursor="hand2"
                                                  , takefocus=False, command=toggle_theme)
left_settings_theme_label.pack(side=LEFT, padx=(6, 0), pady=(2, 0))
left_settings_theme_button.pack(side=LEFT, padx=(6, 0), pady=(2, 0))
left_settings_frame_third.pack(fill=X)
# end
# fourth setting
left_settings_frame_fourth: ClassVar = Frame(left_settings_frame)
left_settings_buffer_label: ClassVar = ttk.Label(left_settings_frame_fourth, text="Use double buffer",
                                                 font='Bahnschrift 11'
                                                 , style="W.TLabel")
left_settings_buffer_button: ClassVar = ttk.Button(left_settings_frame_fourth, cursor="hand2", takefocus=False
                                                   , command=toggle_buffer)
left_settings_buffer_label.pack(side=LEFT, padx=(6, 0), pady=(0, 0))
left_settings_buffer_button.pack(side=LEFT, padx=(6, 0), pady=(0, 0))
left_settings_frame_fourth.pack(anchor=W, fill=X)
# end
# fifth setting
left_settings_frame_fifth: ClassVar = Frame(left_settings_frame)
left_settings_continue_label: ClassVar = ttk.Label(left_settings_frame_fifth, text="Continue where I left off",
                                                   font='Bahnschrift 11'
                                                   , style="W.TLabel")
left_settings_continue_button: ClassVar = ttk.Button(left_settings_frame_fifth, cursor="hand2", takefocus=False,
                                                     command=toggle_continue)
left_settings_continue_label.pack(side=LEFT, padx=(6, 0), pady=(0, 0))
left_settings_continue_button.pack(side=LEFT, padx=(6, 0), pady=(0, 0))
left_settings_frame_fifth.pack(anchor=W, fill=X)
# end
settings_version_label: ClassVar = ttk.Label(left_settings_frame, text="V" + version + " Sounder © by Mateusz Perczak",
                                             font='Bahnschrift 11', style="W.TLabel")
settings_version_label.pack(anchor=SW, padx=(6, 0), pady=(265, 0))
# main frame
main_player_frame: ClassVar = Frame(main_window)
main_player_frame.grid(row=0, column=0, sticky='news')
# end
# top frame
top_player_frame: ClassVar = Frame(main_player_frame)
top_player_refresh_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                 command=refresh_dir)
top_player_folder_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                command=change_dir_btn)
top_player_path_label: ClassVar = ttk.Label(top_player_frame, width=85, textvariable=path, font='Bahnschrift 11',
                                            style="W.TLabel")
top_player_settings_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                  command=lambda: show(main_settings_frame, "main_settings_frame"))
top_player_refresh_button.pack(side=LEFT)
top_player_folder_button.pack(side=LEFT)
top_player_path_label.pack(side=LEFT, padx=0.5)
top_player_settings_button.pack(side=LEFT, padx=6)
top_player_frame.pack(anchor=W)
# end
# bottom_frame
bottom_player_frame: ClassVar = Frame(main_player_frame)
bottom_player_frame.pack(fill=BOTH, expand=True)
# end
# left_frame
left_player_frame: ClassVar = Frame(bottom_player_frame)
left_player_scrollbar_frame: ClassVar = Frame(bottom_player_frame)
left_player_music_scrollbar: ClassVar = ttk.Scrollbar(left_player_frame, orient=HORIZONTAL, cursor="hand2",
                                                      takefocus=False)
left_player_list_box_frame: ClassVar = Frame(left_player_frame)
left_player_music_list: ClassVar = Listbox(left_player_list_box_frame, width=50, height=23, font='Bahnschrift 11',
                                           cursor="hand2"
                                           , bd=0, activestyle="none", takefocus=False, selectmode="SINGLE",
                                           highlightthickness=0
                                           , xscrollcommand=left_player_music_scrollbar.set)
left_player_music_list.pack(side=LEFT, padx=(2, 0), pady=(9, 0))
left_player_list_box_frame.pack(pady=(0, 4))
left_player_music_scrollbar.configure(command=left_player_music_list.xview)
left_player_music_scrollbar.pack(fill=X)
left_player_scrollbar_frame.pack(side=LEFT, fill=X, padx=(2, 0))
left_player_frame.pack(side=LEFT)
# end
# right_frame
right_player_frame: ClassVar = Frame(bottom_player_frame)
right_player_album_label: ClassVar = ttk.Label(right_player_frame, textvariable=album_name, font='Bahnschrift 10',
                                               style="W.TLabel")
right_player_album_art_label: ClassVar = ttk.Label(right_player_frame, font='Bahnschrift 11',
                                                   style="W.TLabel")
right_player_time_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_time, font='Bahnschrift 11',
                                              style="W.TLabel")
right_player_title_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_title, font='Bahnschrift 11',
                                               style="W.TLabel", wraplength=350)
right_player_album_label.pack(pady=(10, 0))
right_player_album_art_label.pack(pady=(2, 0))
right_player_title_label.pack(ipady=2)
right_player_time_label.pack(ipady=2)
right_player_frame.pack()
# end
# buttons_frame
buttons_player_frame: ClassVar = Frame(right_player_frame)
buttons_player_previous_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                      command=lambda: music("previous"))
buttons_player_play_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                  command=lambda: music("play"))
buttons_player_forward_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                     command=lambda: music("forward"))
buttons_player_previous_button.pack(side=LEFT, ipadx=2)
buttons_player_play_button.pack(side=LEFT, ipadx=2)
buttons_player_forward_button.pack(side=LEFT, ipadx=2)
buttons_player_frame.pack(pady=(20, 0))
# end
# mode frame
mode_player_frame: ClassVar = Frame(right_player_frame)
mode_player_mode_button: ClassVar = ttk.Button(right_player_frame, cursor="hand2", takefocus=False,
                                               command=mode_change)
mode_player_mode_button.pack()
mode_player_frame.pack()
# end

show(main_init_frame, "main_init_frame")
init_thread = threading.Thread(target=init_player, )
init_thread.daemon = True
init_thread.start()
left_player_music_list.bind("<<ListboxSelect>>", list_box_selector)
main_window.protocol("WM_DELETE_WINDOW", close)
main_window.mainloop()
