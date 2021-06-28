try:
    import os
    from time import sleep
    from threading import Thread
    from json import dump, load
    import logging
    from requests import get
    from tkinter import Tk, PhotoImage, StringVar, Frame, Entry, Listbox, Toplevel, sys, Text
    from tkinter import ttk
    from tkinter.filedialog import askdirectory
    from pygame import mixer
    from PIL import ImageTk
    from PIL import Image
    from io import BytesIO
    from mutagen.mp3 import MP3
    from typing import ClassVar, Dict
    from random import shuffle, choice, sample
    from re import findall
except ImportError as e:
    sys.exit(e)

# dir
sounder_dir: str = os.getcwd()
# sounder_dir: str = os.path.dirname(sys.executable)
user_path: str = os.path.expanduser("~")
# end
main_window: ClassVar = Tk()
main_window.withdraw()
main_window.geometry("806x500")
main_window.title("Sounder3")
main_window.iconbitmap(sounder_dir + "\\icon.ico")
main_window.resizable(width=False, height=False)
# icons
logo_1_img: ClassVar = PhotoImage(file=sounder_dir + "\\logo_1.png")
error_img: ClassVar = PhotoImage(file=sounder_dir + "\\error_light.png")
# end
# var
music_title: ClassVar = StringVar()
music_artist: ClassVar = StringVar()
music_position: ClassVar = StringVar()
music_total: ClassVar = StringVar()
album_name: ClassVar = StringVar()
error_reason: ClassVar = StringVar()
music_bitrate: ClassVar = StringVar()
debug_info: ClassVar = StringVar()
config: Dict = {}
version: str = "3.2.0"
played_songs: list = []
songs: list = []
search_list: list = []
current_song: int = 0
random_list: list = []
play_button_state: bool = False
default_album_img: ClassVar
repeat_all_img: ClassVar
repeat_one_img: ClassVar
repeat_none_img: ClassVar
shuffle_play_img: ClassVar
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
close_img: ClassVar


# end
# functions
# errors
def error_dump(error_obj: ClassVar) -> None:
    try:
        if mixer.music.get_busy():
            mixer.music.pause()
    except:
        pass
    error_reason.set(logging.getLevelName(error_obj))
    show(main_error_frame)
    logging.error(error_obj, exc_info=True)


# end


def load_settings() -> bool:
    global config, version, sounder_dir
    config = {"refresh_time": 1.0, "theme": "light", "version": version, "transition_duration": 1,
              "fst_buffer": False, "mode": "r_n",
              "last_song": "", "continue": False, "folders": [user_path + "\\Music"], "fade": False, "debug": False,
              "update": True}
    if os.path.isfile("cfg.json"):
        try:
            with open('cfg.json', 'r') as data:
                config = load(data)
            return True
        except:
            pass
    with open('cfg.json', 'w') as data:
        dump(config, data)
    return True


def save_settings() -> bool:
    global config
    if os.path.isfile('cfg.json'):
        try:
            with open('cfg.json', 'w') as data:
                dump(config, data)
            return True
        except Exception as e:
            error_dump(e)
            return False


def sort_by_letter(element) -> str:
    return os.path.splitext((os.path.basename(element)))[0][0].lower()


def load_music() -> bool:
    global config, songs, random_list, played_songs
    songs = []
    played_songs = []
    try:
        for folder in config["folders"]:
            for file in os.listdir(folder):
                if file.endswith(".xm") or file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg") or file.endswith(".flac"):
                    songs.append(os.path.abspath(os.path.join(folder, file)))
        random_list = list(range(0, len(songs)))
        shuffle(random_list)
        songs.sort(key=sort_by_letter)
    except:
        return False
    return True


# directory


def folders() -> None:
    global config
    folder_window: ClassVar = Toplevel()
    folder_window.withdraw()
    folder_window.grab_set()
    folder_window.title("Folders")
    folder_window.geometry(f"400x400+{main_window.winfo_x() + 215}+{main_window.winfo_y() + 50}")
    folder_window.minsize(400, 300)
    folder_window.iconbitmap(sounder_dir + "\\icon.ico")
    folder_window.resizable(width=False, height=True)
    if config["theme"] == "light":
        folder_window.configure(background="#fff")
    elif config["theme"] == "dark":
        folder_window.configure(background="#000")
    update_folders(folder_window)
    folder_window.deiconify()
    folder_window.mainloop()


def update_folders(window_obj: ClassVar) -> None:
    global config
    color: list = []
    y: int = 100
    if config["theme"] == "light":
        color = ["#000", "#fff"]
    elif config["theme"] == "dark":
        color = ["#1e88e5", "#000"]
    for widget in window_obj.winfo_children():
        widget.destroy()
    music_label: ClassVar = ttk.Label(window_obj, text="Music on this computer", font='Bahnschrift 11')
    music_label.place(relx=0.5, y=2, anchor='n')
    add_folder_button: ClassVar = ttk.Button(window_obj, text="+ Add folder", cursor="hand2", takefocus=False,
                                             command=lambda: add_folder(window_obj))
    add_folder_button.place(relx=0.5, y=50, anchor='n')
    for folder in config["folders"]:
        add_card(folder, window_obj, color, y)
        y += 65


def add_card(path: str, window_obj: ClassVar, color: list, y: int) -> ClassVar:
    card: ClassVar = Frame(window_obj, background=color[0], relief='flat')
    card_frame: ClassVar = Frame(card, background=color[1], relief='flat')
    name_label: ClassVar = ttk.Label(card_frame, text=os.path.basename(os.path.normpath(path)), font='Bahnschrift 11')
    path_label: ClassVar = ttk.Label(card_frame, text=path, font='Bahnschrift 10')
    remove_button: ClassVar = ttk.Button(card_frame, image=close_img, text="Remove", cursor="hand2", takefocus=False
                                         , compound='top')
    remove_button.configure(command=lambda: remove_card(card, window_obj, path))
    name_label.place(relx=0.01, rely=0.08)
    path_label.place(relx=0.01, rely=0.5)
    remove_button.place(relx=0.67, rely=0, relheight=1)
    card_frame.place(relx=0.5, y=1, height=58, width=278, anchor='n')
    card.place(relx=0.5, y=y, height=60, width=280, anchor='n')
    return card


def remove_card(card: ClassVar, window_obj: ClassVar, path: str) -> None:
    global config
    config["folders"].remove(path)
    card.destroy()
    update_folders(window_obj)


def add_folder(window_obj: ClassVar) -> None:
    global config
    folder: str = askdirectory()
    if bool(folder) and not folder in config["folders"]:
        config["folders"].append(folder)
        update_folders(window_obj)
        refresh_dir()


# end
def refresh_window() -> None:
    global songs, current_song, search_list
    left_player_music_list.delete(0, 'end')
    if bool(songs) and bool(search_list):
        for song in search_list:
            left_player_music_list.insert(len(search_list), os.path.splitext(os.path.basename(song))[0])
        left_player_music_list.select_set(search_list.index(songs[current_song]))
        left_player_music_list.see(search_list.index(songs[current_song]))
    elif bool(songs) and not bool(search_list):
        for song in songs:
            left_player_music_list.insert(len(songs), os.path.splitext(os.path.basename(song))[0])
        left_player_music_list.select_set(current_song)
        left_player_music_list.see(current_song)


def init_music() -> bool:
    global config, songs, current_song
    try:
        if bool(songs):
            if config["last_song"] in songs:
                current_song = songs.index(config["last_song"])
                if config["continue"]:
                    play()
                else:
                    set_song_attrib()
            else:
                set_song_attrib()
        return True
    except Exception as e:
        error_dump(e)
        return False


def refresh_dir() -> None:
    if load_music():
        refresh_window()


def verify_settings() -> None:
    global config, user_path, version
    try:
        if not type(config["theme"]) is str:
            config["theme"] = "light"
    except:
        config["theme"] = "light"
    try:
        if not type(config["version"]) is str:
            config["version"] = version
        elif int(config["version"].replace(".", "")) < int(version.replace(".", "")):
            config["version"] = version
    except:
        config["version"] = version
    try:
        if not type(config["fst_buffer"]) is bool:
            config["fst_buffer"] = False
    except:
        config["fst_buffer"] = False
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
    try:
        if not type(config["fade"]) is bool:
            config["fade"] = False
    except:
        config["fade"] = False
    try:
        if not type(config["mode"]) is str:
            config["mode"] = "r_n"
    except:
        config["mode"] = "r_n"
    try:
        if not type(config["debug"]) is bool:
            config["debug"] = False
    except:
        config["debug"] = False
    try:
        if not type(config["folders"]) is list:
            config["folders"] = (user_path + "\\Music").replace('/', '\\')
    except:
        config["path"] = (user_path + "\\Music").replace('/', '\\')
    try:
        if not type(config["update"]) is bool:
            config["update"] = True
    except:
        config["update"] = True


def apply_theme() -> bool:
    global config, repeat_all_img, repeat_one_img, repeat_none_img, forward_img, play_img, previous_img, pause_img \
        , toggle_off_img, toggle_on_img, default_album_img, settings_img, back_img, folder_img, refresh_img \
        , play_button_state, shuffle_play_img, close_img
    main_theme = ttk.Style()
    main_theme.theme_use('clam')
    try:
        if config["theme"] == "light":
            main_theme.configure("TLabel", background='#fff', foreground='#000', border='0')
            main_theme.configure("Horizontal.TProgressbar", foreground='#000', background='#000', lightcolor='#fff'
                                 , darkcolor='#fff', bordercolor='#fff', troughcolor='#fff')
            main_theme.configure("TButton", background='#fff', relief="flat", font=('Bahnschrift', 10),
                                 foreground='#000')
            main_theme.map("TButton", background=[('pressed', '!disabled', '#fff'), ('active', '#eee')])
            main_theme.map("TScale", background=[('pressed', '!disabled', '#111'), ('active', '#111')])
            main_theme.configure("TScale", troughcolor='#eee', background='#000', relief="flat", gripcount=0,
                                 darkcolor="#eee", lightcolor="#eee", bordercolor="#eee")
            main_theme.configure("Horizontal.TScrollbar", gripcount=0, relief="flat",
                                 background="#fff", darkcolor="#fff", lightcolor="#fff",
                                 troughcolor="#fff", bordercolor="#fff", arrowcolor="#000")
            main_theme.map("Horizontal.TScrollbar", background=[('pressed', '!disabled', '#eee'), ('active', '#eee')])
            left_player_music_list.configure(selectbackground="#000", foreground='#000', background='#fff',
                                             relief="flat")
            top_player_search_box.configure(selectbackground="#000", selectforeground="#fff", background="#fff"
                                            , foreground="#000")
            main_player_frame.configure(background="#fff")
            buttons_player_frame.configure(background="#fff")
            right_player_frame.configure(background="#fff")
            bottom_player_frame.configure(background="#fff")
            top_player_frame.configure(background="#fff")
            settings_frame_third.configure(background="#fff")
            settings_bar_frame.configure(background="#fff")
            main_settings_frame.configure(background="#fff")
            settings_frame_fourth.configure(background="#fff")
            main_window.configure(background="#fff")
            settings_frame_fifth.configure(background="#fff")
            settings_frame_sixth.configure(background="#fff")
            settings_frame_seventh.configure(background="#fff")
            left_player_frame.configure(background="#fff")
            bottom_time_frame.configure(background="#fff")
            top_search_frame.configure(background="#000")
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
            shuffle_play_img = PhotoImage(file=sounder_dir + "\\shuffle_light.png")
            close_img = PhotoImage(file=sounder_dir + "\\close_light.png")
            top_player_delete_button.configure(image=close_img)
            right_player_album_art_label.configure(image=default_album_img)
            mode_player_mode_button.configure(image=repeat_none_img)
            buttons_player_forward_button.configure(image=forward_img)
            if play_button_state:
                buttons_player_play_button.configure(image=pause_img)
            else:
                buttons_player_play_button.configure(image=play_img)
            buttons_player_previous_button.configure(image=previous_img)
            top_player_settings_button.configure(image=settings_img)
            settings_back_button.configure(image=back_img)
            top_player_folder_button.configure(image=folder_img)
            top_player_refresh_button.configure(image=refresh_img)
            third_settings_theme_button.configure(image=toggle_off_img)
            if config["fst_buffer"]:
                fourth_settings_buffer_button.configure(image=toggle_on_img)
            else:
                fourth_settings_buffer_button.configure(image=toggle_off_img)
            if config["mode"] == "r_n":
                mode_player_mode_button.configure(image=repeat_none_img)
            elif config["mode"] == "r_a":
                mode_player_mode_button.configure(image=repeat_all_img)
            elif config["mode"] == "r_o":
                mode_player_mode_button.configure(image=repeat_one_img)
            elif config["mode"] == "s_p":
                mode_player_mode_button.configure(image=shuffle_play_img)
            if config["continue"]:
                fifth_settings_continue_button.configure(image=toggle_on_img)
            else:
                fifth_settings_continue_button.configure(image=toggle_off_img)
            if config["fade"]:
                sixth_settings_fade_button.configure(image=toggle_on_img)
            else:
                sixth_settings_fade_button.configure(image=toggle_off_img)
            if config["update"]:
                seventh_settings_update_button.configure(image=toggle_on_img)
            else:
                seventh_settings_update_button.configure(image=toggle_off_img)
        elif config["theme"] == "dark":
            main_theme.configure("TLabel", foreground='#fff', background='#000', border='0')
            main_theme.configure("Horizontal.TProgressbar", foreground='#000', background='#1e88e5', lightcolor='#000'
                                 , darkcolor='#000', bordercolor='#000', troughcolor='#000')
            main_theme.configure("TButton", relief="flat", background='#000',
                                 font=('Bahnschrift', 10), foreground='#fff')
            main_theme.map("TButton", background=[('pressed', '!disabled', '#000'), ('active', '#111')])
            main_theme.map("TScale", background=[('pressed', '!disabled', '#0d77d4'), ('active', '#0d77d4')])
            main_theme.configure("TScale", troughcolor='#111', background='#1e88e5', relief="flat",
                                 gripcount=0, darkcolor="#111", lightcolor="#111", bordercolor="#000")
            main_theme.configure("Horizontal.TScrollbar", gripcount=0, relief="flat", background="#000",
                                 darkcolor="#000", lightcolor="#000", troughcolor="#000", bordercolor="#000",
                                 arrowcolor="#1e88e5")
            main_theme.map("Horizontal.TScrollbar", background=[('pressed', '!disabled', '#111'), ('active', '#111')])
            left_player_music_list.configure(selectbackground="#1e88e5", foreground='#fff', background='#000',
                                             relief="flat")
            top_player_search_box.configure(selectbackground="#1e88e5", selectforeground="#fff", background="#000"
                                            , foreground="#fff")
            top_search_frame.configure(background="#1e88e5")
            main_player_frame.configure(background="#000")
            buttons_player_frame.configure(background="#000")
            right_player_frame.configure(background="#000")
            bottom_player_frame.configure(background="#000")
            top_player_frame.configure(background="#000")
            settings_frame_third.configure(background="#000")
            settings_bar_frame.configure(background="#000")
            main_settings_frame.configure(background="#000")
            settings_frame_fourth.configure(background="#000")
            main_window.configure(background="#000")
            settings_frame_fifth.configure(background="#000")
            settings_frame_sixth.configure(background="#000")
            settings_frame_seventh.configure(background="#000")
            left_player_frame.configure(background="#000")
            bottom_time_frame.configure(background="#000")
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
            shuffle_play_img = PhotoImage(file=sounder_dir + "\\shuffle_dark.png")
            close_img = PhotoImage(file=sounder_dir + "\\close_dark.png")
            top_player_delete_button.configure(image=close_img)
            right_player_album_art_label.configure(image=default_album_img)
            mode_player_mode_button.configure(image=repeat_none_img)
            buttons_player_forward_button.configure(image=forward_img)
            if play_button_state:
                buttons_player_play_button.configure(image=pause_img)
            else:
                buttons_player_play_button.configure(image=play_img)
            buttons_player_previous_button.configure(image=previous_img)
            top_player_settings_button.configure(image=settings_img)
            settings_back_button.configure(image=back_img)
            top_player_folder_button.configure(image=folder_img)
            top_player_refresh_button.configure(image=refresh_img)
            third_settings_theme_button.configure(image=toggle_on_img)
            if config["fst_buffer"]:
                fourth_settings_buffer_button.configure(image=toggle_on_img)
            else:
                fourth_settings_buffer_button.configure(image=toggle_off_img)
            if config["mode"] == "r_n":
                mode_player_mode_button.configure(image=repeat_none_img)
            elif config["mode"] == "r_a":
                mode_player_mode_button.configure(image=repeat_all_img)
            elif config["mode"] == "r_o":
                mode_player_mode_button.configure(image=repeat_one_img)
            elif config["mode"] == "s_p":
                mode_player_mode_button.configure(image=shuffle_play_img)
            if config["continue"]:
                fifth_settings_continue_button.configure(image=toggle_on_img)
            else:
                fifth_settings_continue_button.configure(image=toggle_off_img)
            if config["fade"]:
                sixth_settings_fade_button.configure(image=toggle_on_img)
            else:
                sixth_settings_fade_button.configure(image=toggle_off_img)
            if config["update"]:
                seventh_settings_update_button.configure(image=toggle_on_img)
            else:
                seventh_settings_update_button.configure(image=toggle_off_img)
        else:
            config["theme"] = "light"
            return False
        return True
    except Exception as e:
        error_dump(e)
        return False


def debug(char) -> None:
    global config, play_button_state, songs, played_songs
    if char.keysym == "F12":
        show(main_debug_screen)
        debug_info.set(f"theme: {config['theme']}"
                       f"version: {config['version']}"
                       f"fst_buffer: {config['fst_buffer']} mode: {config['mode']} continue: {config['continue']} "
                       f"fade: {config['fade']} debug: {config['debug']} music_title: {music_title.get()} "
                       f"music_artist: {music_artist.get()} music_position: {music_position.get()} "
                       f"music_total: {music_total.get()} album_name: {album_name.get()} num_of_songs: {len(songs)} "
                       f"current_song: {current_song} play_button_state: {play_button_state}\n"
                       f"played_songs: {played_songs}\nsongs: {songs}")


def apply_settings() -> bool:
    global config
    try:
        music_position.set("--:--")
        music_total.set("--:--")
        music_bitrate.set("---")
        debug_info.set("")
        if config["fade"]:
            main_window.attributes('-alpha', 0.8)
        if config["debug"]:
            main_window.bind('<F12>', debug)
        if config["update"]:
            Thread(target=check_for_update, daemon=True).start()
        logging.basicConfig(filename=f"{sounder_dir}\\errors.log", level=logging.ERROR)
    except Exception as e:
        error_dump(e)
        return False
    return True


def init_mixer() -> bool:
    global config
    try:
        if config["fst_buffer"]:
            mixer.pre_init(frequency=44100, size=16, channels=2, buffer=3072, devicename=None)
        else:
            mixer.pre_init(frequency=44100, size=16, channels=2, buffer=4096, devicename=None)
        mixer.init()
        mixer.music.set_volume(1)
    except Exception as e:
        error_dump(e)
        return False
    try:
        Thread(target=song_stats, daemon=True).start()
    except Exception as e:
        error_dump(e)
        return False
    return True


def init_player() -> None:
    try:
        if load_settings():
            verify_settings()
            if apply_settings():
                if apply_theme():
                    if init_mixer():
                        if load_music():
                            if init_music():
                                refresh_window()
                                show(main_player_frame)
    except Exception as e:
        error_dump(e)


def forward() -> None:
    global songs, play_button_state, current_song, config, random_list, played_songs
    try:
        if bool(songs):
            if config["mode"] == "s_p" and (len(songs)) > 2:
                current_song = choice(sample(random_list, k=int(len(songs) / 2)))
                while current_song in played_songs:
                    if len(played_songs) == len(songs):
                        played_songs = []
                    current_song = choice(sample(random_list, k=int(len(songs) / 2)))
                played_songs.append(current_song)
            elif not current_song >= len(songs) - 1:
                current_song += 1
            if mixer.music.get_busy():
                mixer.music.stop()
            mixer.music.load(songs[current_song])
            mixer.music.play()
            set_song_attrib()
            if not play_button_state:
                play_button_state = True
                buttons_player_play_button.configure(image=pause_img)
            left_player_music_list.see(current_song)
    except:
        refresh_dir()


def previous() -> None:
    global songs, play_button_state, current_song, played_songs
    try:
        if bool(songs):
            if config["mode"] == "s_p" and (len(songs)) > 2 and bool(played_songs):
                if len(played_songs) > 1:
                    current_song = played_songs[-2]
                elif len(played_songs) == 1:
                    current_song = played_songs[-1]
                played_songs.remove(current_song)
            elif not current_song <= 0:
                current_song -= 1
            if mixer.music.get_busy():
                mixer.music.stop()
            mixer.music.load(songs[current_song])
            mixer.music.play()
            set_song_attrib()
            if not play_button_state:
                play_button_state = True
                buttons_player_play_button.configure(image=pause_img)
            left_player_music_list.see(current_song)
    except:
        refresh_dir()


def list_box_play(event=None) -> None:
    global songs, play_button_state, current_song, search_list
    try:
        if bool(songs) and bool(search_list):
            current_song = songs.index(search_list[left_player_music_list.curselection()[0]])
            clear_search()
        elif bool(songs) and bool(left_player_music_list.curselection()):
            current_song = left_player_music_list.curselection()[0]
        if bool(songs):
            if play_button_state:
                if mixer.music.get_busy():
                    mixer.music.stop()
            elif not play_button_state:
                play_button_state = True
                buttons_player_play_button.configure(image=pause_img)
            mixer.music.load(songs[current_song])
            mixer.music.play()
            set_song_attrib()
    except Exception:
        refresh_dir()


def play() -> None:
    global songs, play_button_state, current_song
    try:
        if bool(songs):
            if play_button_state and mixer.music.get_busy():
                play_button_state = False
                mixer.music.pause()
                buttons_player_play_button.configure(image=play_img)
            elif not play_button_state and not mixer.music.get_busy():
                play_button_state = True
                mixer.music.load(songs[current_song])
                mixer.music.play()
                set_song_attrib()
                buttons_player_play_button.configure(image=pause_img)
            elif not play_button_state and mixer.music.get_busy():
                play_button_state = True
                mixer.music.unpause()
                buttons_player_play_button.configure(image=pause_img)
        elif not bool(songs) and play_button_state:
            play_button_state = False
            mixer.music.stop()
            buttons_player_play_button.configure(image=play_img)
    except:
        refresh_dir()


def set_song_attrib() -> None:
    global songs, current_song, album_img, config, search_list
    if bool(songs):
        if os.path.splitext(songs[current_song])[1] == ".mp3":
            try:
                tags: ClassVar = MP3(songs[current_song])
                try:
                    bottom_player_progress_bar["maximum"] = tags.info.length
                    music_total.set(str(int(divmod(tags.info.length, 60)[0])) + ":"
                                    + str(int(divmod(tags.info.length, 60)[1])).zfill(2))
                except:
                    music_total.set("--:--")
                try:
                    album: str = tags["TALB"]
                    album_name.set(album)
                except:
                    album_name.set("")
                try:
                    music_bitrate.set(f"{int(tags.info.bitrate / 1000)}")
                except:
                    music_bitrate.set("---")
                try:
                    pict: bytes = tags.get("APIC:").data
                    album_img = ImageTk.PhotoImage(Image.open(BytesIO(pict)).resize((220, 220)))
                    right_player_album_art_label.configure(image=album_img)
                except:
                    right_player_album_art_label.configure(image=default_album_img)
                try:
                    right_player_title_label.configure(font='Bahnschrift 11')
                    music_title.set(f"{tags['TIT2']}")
                except:
                    if len(songs[current_song]) > 50:
                        right_player_title_label.configure(font='Bahnschrift 9')
                    else:
                        right_player_title_label.configure(font='Bahnschrift 11')
                    music_title.set(os.path.splitext(os.path.basename(songs[current_song]))[0])
                try:
                    music_artist.set(tags["TPE1"])
                except:
                    music_artist.set("")
            except:
                right_player_album_art_label.configure(image=default_album_img)
                if len(songs[current_song]) > 50:
                    right_player_title_label.configure(font='Bahnschrift 9')
                else:
                    right_player_title_label.configure(font='Bahnschrift 11')
                music_title.set(os.path.splitext(os.path.basename(songs[current_song]))[0])
                music_artist.set("")
            left_player_music_list.selection_clear(0, 'end')
            if not bool(search_list):
                left_player_music_list.select_set(current_song)
            music_position.set("0:00")
        else:
            bottom_player_progress_bar["maximum"] = 999999
            album_name.set("")
            music_artist.set("")
            right_player_album_art_label.configure(image=default_album_img)
            if len(songs[current_song]) > 50:
                right_player_title_label.configure(font='Bahnschrift 9')
            else:
                right_player_title_label.configure(font='Bahnschrift 11')
            music_title.set(os.path.splitext(os.path.basename(songs[current_song]))[0])
            left_player_music_list.selection_clear(0, 'end')
            left_player_music_list.select_set(current_song)
            music_position.set("0:00")
            music_total.set("--:--")
            music_bitrate.set("---")
        config["last_song"] = songs[current_song]


def song_stats() -> None:
    global play_button_state, config
    loop: bool = False
    try:
        while True:
            if mixer.music.get_busy() and play_button_state:
                bottom_player_progress_bar["value"] = mixer.music.get_pos() / 1000

                music_position.set(str(int(divmod((mixer.music.get_pos() / 1000), 60)[0])) + ":" + str(int(divmod((mixer.music.get_pos() / 1000), 60)[1])).zfill(2))
                sleep(1)
            elif not mixer.music.get_busy() and play_button_state:
                play_button_state = False
                loop = True
                buttons_player_play_button.configure(image=play_img)
            elif loop and not mixer.music.get_busy() and not play_button_state:
                loop = False
                play_loop()
            else:
                sleep(2)
    except Exception as e:
        error_dump(e)


def play_loop() -> None:
    global config, current_song
    if config["mode"] == "r_n" or config["mode"] == "s_p":
        forward()
    elif config["mode"] == "r_o":
        play()
    elif config["mode"] == "r_a":
        if current_song < (len(songs) - 1):
            forward()
        else:
            current_song = 0
            play()


def mode_change() -> None:
    global config
    if config["mode"] == "r_n":
        config["mode"] = "r_a"
        mode_player_mode_button.configure(image=repeat_all_img)
    elif config["mode"] == "r_a":
        config["mode"] = "r_o"
        mode_player_mode_button.configure(image=repeat_one_img)
    elif config["mode"] == "r_o":
        config["mode"] = "s_p"
        mode_player_mode_button.configure(image=shuffle_play_img)
    elif config["mode"] == "s_p":
        config["mode"] = "r_n"
        mode_player_mode_button.configure(image=repeat_none_img)


def show(window) -> bool:
    try:
        window.tkraise()
        return True
    except Exception as e:
        error_dump(e)
        return False


def check_for_update() -> None:
    global version, sounder_dir, config
    try:
        if os.path.isfile(sounder_dir + "\\Updater.exe"):
            server_version = get("https://raw.githubusercontent.com/losek1/Sounder3/master/updates/version.txt").text
            if int(version.replace(".", "")) < int(server_version.replace(".", "")):
                main_window.after_idle(update_choice)
        else:
            config["update"] = False
    except:
        pass


def update_choice() -> None:
    try:
        update_window: ClassVar = Toplevel()
        update_window.withdraw()
        update_window.grab_set()
        update_window.title("Update Available")
        update_window.geometry(f"375x100+{main_window.winfo_x() + 215}+{main_window.winfo_y() + 200}")
        update_window.iconbitmap(sounder_dir + "\\icon.ico")
        update_window.resizable(width=False, height=False)
        update_window.configure(background="#fff")
        choice_label: ClassVar = ttk.Label(update_window, text="A new version of Sounder is available.\n"
                                                               "Would you like to install it?", font='Bahnschrift 11',
                                           anchor='center', justify='center')
        choice_label.configure(background="#fff", foreground="#000")
        choice_install_button: ClassVar = ttk.Button(update_window, text="UPDATE NOW", cursor="hand2", takefocus=False,
                                                     command=lambda: close("update"))
        choice_exit_button: ClassVar = ttk.Button(update_window, text="UPDATE LATER", cursor="hand2", takefocus=False,
                                                  command=lambda: update_window.destroy())
        choice_label.place(relx=0.5, rely=0.1, anchor="n")
        choice_install_button.place(relx=0.7, rely=0.6, anchor="n")
        choice_exit_button.place(relx=0.3, rely=0.6, anchor="n")
        update_window.deiconify()
        update_window.mainloop()
    except Exception as e:
        error_dump(e)


def close(action: str = "close") -> None:
    for widget in main_window.winfo_children():
        widget.destroy()
    main_window.destroy()
    save_settings()
    if action == "restart":
        if os.path.isfile(sys.argv[0]):
            os.startfile(sys.argv[0])
    elif action == "update":
        if os.path.isfile("Updater.exe"):
            os.startfile("Updater.exe")
    logging.shutdown()
    sys.exit()


def open_logs() -> None:
    try:
        main_window.unbind('<F12>')
        if logging.getLogger().isEnabledFor(logging.ERROR):
            logging.shutdown()
        if os.path.isfile("errors.log"):
            os.startfile("errors.log")
    except:
        pass


def change_dir_btn() -> None:
    try:
        if folders():
            refresh_dir()
    except:
        pass



def toggle_theme() -> None:
    global config
    try:
        show(main_init_frame)
        main_init_frame.update()
        sleep(0.1)
        if config["theme"] == "light":
            config["theme"] = "dark"
        elif config["theme"] == "dark":
            config["theme"] = "light"
        if apply_theme():
            show(main_settings_frame)
    except Exception as e:
        error_dump(e)


def toggle_buffer() -> None:
    global config
    try:
        if config["fst_buffer"]:
            fourth_settings_buffer_button.configure(image=toggle_off_img)
            config["fst_buffer"] = False
        else:
            fourth_settings_buffer_button.configure(image=toggle_on_img)
            config["fst_buffer"] = True
    except Exception as e:
        error_dump(e)


def toggle_continue() -> None:
    global config
    try:
        if config["continue"]:
            fifth_settings_continue_button.configure(image=toggle_off_img)
            config["continue"] = False
        else:
            fifth_settings_continue_button.configure(image=toggle_on_img)
            config["continue"] = True
    except Exception as e:
        error_dump(e)


def toggle_fade() -> None:
    global config
    try:
        if config["fade"]:
            sixth_settings_fade_button.configure(image=toggle_off_img)
            config["fade"] = False
            main_window.attributes('-alpha', 1)
        elif not config["fade"]:
            sixth_settings_fade_button.configure(image=toggle_on_img)
            config["fade"] = True
            main_window.attributes('-alpha', 0.8)
    except Exception as e:
        error_dump(e)


def toggle_update() -> None:
    global config
    try:
        if config["update"]:
            seventh_settings_update_button.configure(image=toggle_off_img)
            config["update"] = False
        elif not config["update"]:
            seventh_settings_update_button.configure(image=toggle_on_img)
            config["update"] = True
    except Exception as e:
        error_dump(e)


def changelog() -> None:
    global sounder_dir, config
    changelog_window: ClassVar = Toplevel()
    changelog_window.withdraw()
    changelog_window.title("Sounder Changelog")
    changelog_window.geometry('450x350+{0}+{1}'.format(main_window.winfo_x() + 178, main_window.winfo_y() + 75))
    changelog_window.iconbitmap(sounder_dir + "\\icon.ico")
    changelog_window.grab_set()
    changelog_window.resizable(width=False, height=False)
    changelog_label: ClassVar = ttk.Label(changelog_window, text="What's new?", font=('Bahnschrift', 14), anchor='center')
    changelog_text: ClassVar = Text(changelog_window, bd=0, cursor="arrow", takefocus=0, font=('Bahnschrift', 10))
    changelog_label.place(relx=0.5, rely=0.01, relwidth=1, relheight=0.1, anchor="n")
    changelog_text.place(relx=0.5, rely=0.21, relwidth=1, relheight=0.8, anchor="n")
    if config["fade"]:
        changelog_window.attributes('-alpha', 0.8)
    if config["theme"] == "light":
        changelog_label.configure(background="#fff", foreground="#000")
        changelog_text.configure(selectbackground="#fff", selectforeground="#000")
        changelog_window.configure(background="#fff")
    else:
        changelog_text.configure(selectbackground="#000", selectforeground="#fff", background="#000", foreground="#fff")
        changelog_window.configure(background="#000")
        changelog_label.configure(background="#000", foreground="#fff")
    if os.path.isfile('changelog.txt'):
        with open('changelog.txt', 'r') as text:
            for line in text.readlines():
                changelog_text.insert('end', line)
        changelog_text.configure(state='disabled')
    changelog_text.insert('end', "[File not found!]")
    changelog_window.deiconify()
    changelog_window.mainloop()


def search(e=None) -> None:
    global songs, search_list, current_song
    if bool(songs) and bool(top_player_search_box.get()):
        search_list = []
        left_player_music_list.select_clear(0, 'end')
        left_player_music_list.delete(0, 'end')
        for song in songs:
            if bool(findall(top_player_search_box.get().lower(), song.lower())):
                left_player_music_list.insert(len(songs), os.path.splitext(os.path.basename(song))[0])
                search_list.append(song)
        if bool(search_list) and songs[current_song] in search_list:
            left_player_music_list.select_set(search_list.index(songs[current_song]))
    else:
        search_list = []
        refresh_window()


def clear_search() -> None:
    global search_list
    if bool(search_list):
        search_list = []
        top_player_search_box.delete(0, 'end')
        refresh_window()


def search_hover(event) -> None:
    global search_list
    if str(event.type) == "FocusIn" and top_player_search_box.get() == "Search here" and not bool(search_list):
        top_player_search_box.delete(0, 'end')
    elif str(event.type) == "FocusOut":
        top_player_search_box.delete(0, 'end')
        top_player_search_box.insert(0, 'Search here')


# end
# frames
# debug screen
main_debug_screen: ClassVar = Frame(main_window)
main_debug_screen.configure(background="#000")
label_debug: ClassVar = ttk.Label(main_debug_screen, text="Debug Screen", font='Bahnschrift 24', background='#000',
                                  foreground='#fff', border='0', anchor="center")
panic_button: ClassVar = ttk.Button(main_debug_screen, cursor="hand2", takefocus=False, text="PANIC",
                                    command=lambda: show(main_error_frame))
restart_button: ClassVar = ttk.Button(main_debug_screen, cursor="hand2", takefocus=False, text="RESTART"
                                      , command=lambda: close("restart"))
main_init_button: ClassVar = ttk.Button(main_debug_screen, text="SHOW MAIN INIT FRAME", cursor="hand2", takefocus=False
                                        , command=lambda: show(main_init_frame))
main_settings_button: ClassVar = ttk.Button(main_debug_screen, text="SHOW MAIN SETTINGS FRAME", cursor="hand2",
                                            takefocus=False
                                            , command=lambda: show(main_settings_frame))

main_player_button: ClassVar = ttk.Button(main_debug_screen, text="SHOW MAIN PLAYER FRAME", cursor="hand2"
                                          , takefocus=False,
                                          command=lambda: show(main_player_frame))
check_for_update_button: ClassVar = ttk.Button(main_debug_screen, text="CHECK FOR UPDATES", cursor="hand2"
                                               , takefocus=False,
                                               command=check_for_update)
info_label: ClassVar = ttk.Label(main_debug_screen, textvariable=debug_info, font='Consolas 8', background='#000',
                                 foreground='#fff', border='0', anchor="n", wraplength=800)
label_debug.place(relx=0.5, rely=0, relwidth=1, relheight=0.15, anchor="n")
panic_button.place(relx=0.7, rely=0.2, relheight=0.08, relwidth=0.3, anchor="n")
restart_button.place(relx=0.7, rely=0.3, relheight=0.08, relwidth=0.3, anchor="n")
main_init_button.place(relx=0.3, rely=0.2, relheight=0.08, relwidth=0.3, anchor="n")
main_settings_button.place(relx=0.3, rely=0.4, relheight=0.08, relwidth=0.3, anchor="n")
main_player_button.place(relx=0.3, rely=0.3, relheight=0.08, relwidth=0.3, anchor="n")
check_for_update_button.place(relx=0.7, rely=0.4, relheight=0.08, relwidth=0.3, anchor="n")
info_label.place(relx=0.005, rely=0.55, relheight=0.44, relwidth=0.99)
main_debug_screen.place(relx=0.5, rely=0, anchor="n", width=806, height=500)
# end
# main init frame
main_init_frame: ClassVar = Frame(main_window)
main_init_frame.configure(background="#fff")
logo_label: ClassVar = ttk.Label(main_init_frame, image=logo_1_img, font='Bahnschrift 11', background='#fff'
                                 , foreground='#000', border='0')
version_label: ClassVar = ttk.Label(main_init_frame, text="V" + version, font='Bahnschrift 11', background='#fff'
                                    , foreground='#000', border='0', anchor='center')
logo_label.place(relx=0.5, rely=0.35, anchor="n")
version_label.place(relx=0.5, rely=0.52, anchor="n")
main_init_frame.place(relx=0.5, rely=0, anchor="n", width=806, height=500)
# end
# main error frame
main_error_frame: ClassVar = Frame(main_window)
main_error_frame.configure(background="#fff")
error_img_label: ClassVar = ttk.Label(main_error_frame, image=error_img, background='#fff', foreground='#000',
                                      border='0')
error_label: ClassVar = ttk.Label(main_error_frame, font='Bahnschrift 14', text="Error", background='#fff'
                                  , foreground='#000')
error_reason_label: ClassVar = ttk.Label(main_error_frame, textvariable=error_reason, background='#fff'
                                         , foreground='#000', border='0', font='Bahnschrift 13', wraplength=700
                                         , justify='center')
error_info_one: ClassVar = ttk.Label(main_error_frame, background='#fff', foreground='#000', border='0',
                                     font='Bahnschrift 11', text="The application unexpectedly crashed!")
error_info_two: ClassVar = ttk.Label(main_error_frame, background='#fff', foreground='#000', border='0',
                                     font='Bahnschrift 11', text="You can find Diagnostic information in the error log")

error_button: ClassVar = ttk.Button(main_error_frame, cursor="hand2", takefocus=False, text="RESTART",
                                    command=lambda: close("restart"))
error_log_button: ClassVar = ttk.Button(main_error_frame, cursor="hand2", takefocus=False, text="OPEN LOG FILE"
                                        , command=open_logs)
error_version_label: ClassVar = ttk.Label(main_error_frame, text="V" + version, font='Bahnschrift 11'
                                          , background='#fff', foreground='#000', border='6')
error_img_label.place(relx=0.5, rely=0.15, anchor="n")
error_label.place(relx=0.5, rely=0.36, anchor="n")
error_reason_label.place(relx=0.5, rely=0.45, anchor="n")
error_info_one.place(relx=0.5, rely=0.6, anchor="n")
error_info_two.place(relx=0.5, rely=0.64, anchor="n")
error_button.place(relx=0.6, rely=0.76, anchor="n")
error_log_button.place(relx=0.4, rely=0.76, anchor="n")
error_version_label.place(relx=0.96, rely=0.94, anchor="n")
main_error_frame.place(relx=0.5, rely=0, anchor="n", width=806, height=500)
# end
# settings frame
main_settings_frame: ClassVar = Frame(main_window)

settings_bar_frame: ClassVar = Frame(main_settings_frame)

settings_label: ClassVar = ttk.Label(settings_bar_frame, text="Settings", font='Bahnschrift 15')
settings_back_button: ClassVar = ttk.Button(settings_bar_frame, cursor="hand2", takefocus=False,
                                            command=lambda: show(main_player_frame))
settings_label.place(relx=0.005, rely=0.12)
settings_back_button.place(relx=0.9548, rely=0)
settings_bar_frame.place(relx=0, rely=0, width=806, height=38)
main_settings_frame.place(relx=0.5, rely=0, anchor="n", relwidth=1, height=500)
# end
# third setting
settings_frame_third: ClassVar = Frame(main_settings_frame)
third_settings_theme_label: ClassVar = ttk.Label(settings_frame_third, text="Dark theme", font='Bahnschrift 11')
third_settings_theme_button: ClassVar = ttk.Button(settings_frame_third, cursor="hand2", takefocus=False
                                                   , command=toggle_theme)
third_settings_theme_label.pack(side='left', padx=(0, 5))
third_settings_theme_button.pack(side='left', padx=(3, 0))
settings_frame_third.place(relx=0.005, rely=0.08, width=300, height=40)
# end
# fourth setting
settings_frame_fourth: ClassVar = Frame(main_settings_frame)
fourth_settings_buffer_label: ClassVar = ttk.Label(settings_frame_fourth, text="Use faster buffer"
                                                   , font='Bahnschrift 11')
fourth_settings_buffer_button: ClassVar = ttk.Button(settings_frame_fourth, cursor="hand2", takefocus=False
                                                     , command=toggle_buffer)
fourth_settings_buffer_label.pack(side='left', padx=(0, 5))
fourth_settings_buffer_button.pack(side='left', padx=(3, 0))
settings_frame_fourth.place(relx=0.005, rely=0.16, width=300, height=40)
# end
# fifth setting
settings_frame_fifth: ClassVar = Frame(main_settings_frame)
fifth_settings_continue_label: ClassVar = ttk.Label(settings_frame_fifth, text="Resume playback on startup",
                                                    font='Bahnschrift 11')
fifth_settings_continue_button: ClassVar = ttk.Button(settings_frame_fifth, cursor="hand2", takefocus=False,
                                                      command=toggle_continue)
fifth_settings_continue_label.pack(side='left', padx=(0, 5))
fifth_settings_continue_button.pack(side='left', padx=(3, 0))
settings_frame_fifth.place(relx=0.005, rely=0.24, width=300, height=40)
# end
# sixth setting
settings_frame_sixth: ClassVar = Frame(main_settings_frame)
sixth_settings_fade_label: ClassVar = ttk.Label(settings_frame_sixth, text="Enable transparency",
                                                font='Bahnschrift 11')
sixth_settings_fade_button: ClassVar = ttk.Button(settings_frame_sixth, cursor="hand2", takefocus=False,
                                                  command=toggle_fade)
sixth_settings_fade_label.pack(side='left', padx=(0, 5))
sixth_settings_fade_button.pack(side='left', padx=(3, 0))
settings_frame_sixth.place(relx=0.005, rely=0.32, width=300, height=40)
# end
# seventh setting
settings_frame_seventh: ClassVar = Frame(main_settings_frame)
seventh_settings_update_label: ClassVar = ttk.Label(settings_frame_seventh, text="Check for updates",
                                                    font='Bahnschrift 11')
seventh_settings_update_button: ClassVar = ttk.Button(settings_frame_seventh, cursor="hand2", takefocus=False,
                                                      command=toggle_update)
seventh_settings_update_label.pack(side='left', padx=(0, 5))
seventh_settings_update_button.pack(side='left', padx=(3, 0))
settings_frame_seventh.place(relx=0.005, rely=0.4, width=300, height=40)
# end
# sounder changelog
settings_version_button: ClassVar = ttk.Button(main_settings_frame,
                                               text="V" + version, takefocus=False, command=changelog, cursor="hand2")
settings_version_button.place(relx=0.005, rely=0.925, relwidth=0.07)
# author label
settings_author_label: ClassVar = ttk.Label(main_settings_frame, text="Sounder © by Mateusz Perczak"
                                            , font='Bahnschrift 11')
settings_author_label.place(relx=0.5, rely=0.94, anchor="n")
# end
# main frame
main_player_frame: ClassVar = Frame(main_window)
main_player_frame.place(relx=0.5, rely=0, anchor="n", width=806, height=500)

# end
# top frame
top_player_frame: ClassVar = Frame(main_player_frame)
top_player_refresh_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False, command=refresh_dir)
top_player_folder_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                command=change_dir_btn)
top_search_frame: ClassVar = Frame(top_player_frame)
top_player_search_box: ClassVar = Entry(top_search_frame, font=('Bahnschrift', 11), exportselection=1, relief='flat')
top_player_search_box.insert(0, 'Search here')
top_player_search_box.place(relx=0.5, rely=0.05, relwidth=0.993, anchor='n')
top_player_delete_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False
                                                , command=clear_search)
top_player_settings_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                  command=lambda: show(main_settings_frame))
top_player_refresh_button.place(relx=0, rely=0)
top_player_folder_button.place(relx=0.046, rely=0)
top_search_frame.place(relx=0.095, rely=0.17, relwidth=0.35, relheight=0.65)
top_player_delete_button.place(relx=0.45, rely=0.05)
top_player_settings_button.place(relx=0.9548, rely=0)
top_player_frame.place(relx=0, rely=0, width=806, height=36)
# end
# bottom_frame
bottom_player_frame: ClassVar = Frame(main_player_frame)
# left frame
left_player_frame: ClassVar = Frame(bottom_player_frame)
left_player_music_scrollbar: ClassVar = ttk.Scrollbar(left_player_frame, orient="horizontal", cursor="hand2",
                                                      takefocus=False)
left_player_music_list: ClassVar = Listbox(left_player_frame, font='Bahnschrift 11', cursor="hand2"
                                           , bd=0, activestyle="none", takefocus=False, selectmode="SINGLE",
                                           highlightthickness=0, xscrollcommand=left_player_music_scrollbar.set
                                           , exportselection=0)
left_player_music_scrollbar.configure(command=left_player_music_list.xview)
left_player_music_scrollbar.place(relx=0.005, rely=0.95, relwidth=1)
left_player_music_list.place(relx=0.005, rely=0, relwidth=1, relheight=0.94)
left_player_frame.place(relx=0, rely=0, width=403, relheight=1)
# end
# right frame
right_player_frame = Frame(bottom_player_frame)
right_player_album_label: ClassVar = ttk.Label(right_player_frame, textvariable=album_name, font='Bahnschrift 10')
right_player_album_art_label: ClassVar = ttk.Label(right_player_frame, font='Bahnschrift 11', )
right_player_title_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_title, font='Bahnschrift 11'
                                               , wraplength=350)
right_player_artist_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_artist, font='Bahnschrift 10', )
right_player_bitrate_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_bitrate, font='Bahnschrift 8', )
right_player_album_label.place(relx=0.5, rely=0.008, anchor="n")
right_player_album_art_label.place(relx=0.5, rely=0.06, anchor="n")
right_player_title_label.place(relx=0.5, rely=0.55, anchor="n")
right_player_artist_label.place(relx=0.5, rely=0.6, anchor="n")
right_player_bitrate_label.place(relx=0.5, rely=0.65, anchor="n")
right_player_frame.place(relx=0.5, rely=0, width=403, relheight=1)
# end
# buttons_frame
buttons_player_frame: ClassVar = Frame(right_player_frame)
buttons_player_previous_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                      command=previous)
buttons_player_play_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                  command=play)
buttons_player_forward_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                     command=forward)
mode_player_mode_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                               command=mode_change)
buttons_player_previous_button.place(relx=0.03, rely=0)
buttons_player_play_button.place(relx=0.5, rely=0, anchor="n")
buttons_player_forward_button.place(relx=0.67, rely=0)
mode_player_mode_button.place(relx=0.5, rely=0.54, anchor="n")
buttons_player_frame.place(relx=0.5, rely=0.71, anchor="n", relwidth=0.3, relheight=0.15)
# bottom_time_frame
bottom_time_frame: ClassVar = Frame(right_player_frame)
bottom_player_now_label: ClassVar = ttk.Label(bottom_time_frame, textvariable=music_position, font='Bahnschrift 10',
                                              justify='center', anchor='center')
bottom_player_progress_bar: ClassVar = ttk.Progressbar(bottom_time_frame, orient="horizontal", mode="determinate")
bottom_player_end_label: ClassVar = ttk.Label(bottom_time_frame, textvariable=music_total, font='Bahnschrift 10'
                                              , justify='center', anchor='center')
bottom_player_now_label.place(relx=0, rely=0, relwidth=0.08)
bottom_player_progress_bar.place(relx=0.07, rely=0.15, relwidth=0.86, height=15)
bottom_player_end_label.place(relx=0.92, rely=0, relwidth=0.08)
bottom_time_frame.place(relx=0, rely=0.94, relwidth=1, relheight=0.04)
# end
bottom_player_frame.place(relx=0.5, rely=0.09, anchor="n", relwidth=1, height=464)
# end
# main
show(main_init_frame)
init_thread: ClassVar = Thread(target=init_player, daemon=True).start()
# end
left_player_music_list.bind("<<ListboxSelect>>", list_box_play)
top_player_search_box.bind("<KeyRelease>", search)
top_player_search_box.bind("<FocusIn>", search_hover)
top_player_search_box.bind("<FocusOut>", search_hover)
main_window.protocol("WM_DELETE_WINDOW", close)
main_window.deiconify()
main_window.mainloop()