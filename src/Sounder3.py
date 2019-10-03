try:
    import os
    import time
    import threading
    import json
    import logging
    from pygame import mixer
    from tkinter import *
    from tkinter import ttk
    from tkinter.filedialog import askdirectory
    from PIL import ImageTk
    from PIL import Image
    from io import BytesIO
    from mutagen.id3 import ID3
    from mutagen.mp3 import MP3
    from typing import ClassVar, Dict, List
except ImportError:
    sys.exit(1)

# dir
# sounder_dir: str = os.getcwd()
sounder_dir: str = os.path.dirname(sys.executable)
user_path: str = os.path.expanduser("~")
# end
main_window: ClassVar = Tk()
main_window.geometry("806x500")
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
music_artist: ClassVar = StringVar()
music_position: ClassVar = StringVar()
music_total: ClassVar = StringVar()
album_name: ClassVar = StringVar()
error_reason: ClassVar = StringVar()
debug_info: ClassVar = StringVar()
config: Dict = {}
version: str = "3.0.9"
num_of_songs: int = 0
songs: List = []
current_song: int = 0
play_button_state: bool = False
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
music_img: ClassVar
trash_can: ClassVar


# end
# functions
# errors
def dump(error_obj: ClassVar) -> None:
    try:
        if mixer.music.get_busy():
            mixer.music.pause()
    except:
        pass
    error_reason.set(logging.getLevelName(error_obj))
    show(main_error_frame, "main_error_frame")
    logging.error(error_obj, exc_info=True)


# end


def load_settings() -> bool:
    global config, version, sounder_dir
    os.chdir(sounder_dir)
    config = {"refresh_time": 1.0, "theme": "light", "version": version, "transition_duration": 1,
              "gtr_buffer": False, "mode": "r_n",
              "last_song": "", "continue": False, "path": user_path + "\\Music", "fade": False, "debug": False}

    if os.path.isfile('cfg.json'):
        try:
            with open('cfg.json', 'r') as data:
                config = json.load(data)
            return True
        except:
            pass
    with open('cfg.json', 'w') as data:
        json.dump(config, data)
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
            dump(e)
            return False


def load_music() -> bool:
    global config, num_of_songs, songs
    num_of_songs = -1
    songs = []
    try:
        os.chdir(config["path"])
        for file in os.listdir(config["path"]):
            if file.endswith(".xm") or file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg"):
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
        element: str
        for element in songs:
            left_player_music_list.insert(len(songs), os.path.splitext(element)[0])
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
    global config, user_path
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
        if not type(config["transition_duration"]) is float:
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
        if not type(config["path"]) is str:
            config["path"] = (user_path + "\\Music").replace('/', '\\')
        else:
            os.chdir(config["path"])
    except:
        config["path"] = (user_path + "\\Music").replace('/', '\\')


def apply_theme() -> bool:
    global config, repeat_all_img, repeat_one_img, repeat_none_img, forward_img, play_img, previous_img, pause_img \
        , toggle_off_img, toggle_on_img, default_album_img, settings_img, back_img, folder_img, refresh_img \
        , play_button_state
    main_theme = ttk.Style()
    main_theme.theme_use('clam')
    try:
        if config["theme"] == "light":
            main_theme.configure("W.TLabel", background='#fff', foreground='#000', border='0')
            main_theme.configure("W.Horizontal.TProgressbar", foreground='#000', background='#000', lightcolor='#fff'
                                 , darkcolor='#fff', bordercolor='#fff', troughcolor='#fff')
            main_theme.configure("TButton", background='#fff', relief="flat", font=('Bahnschrift', 11),
                                 foreground='#000')
            main_theme.map("TButton", background=[('pressed', '!disabled', '#fff'), ('active', '#eee')])
            main_theme.map("TScale", background=[('pressed', '!disabled', '#111'), ('active', '#111')])
            main_theme.configure("TScale", troughcolor='#eee', background='#000', relief="flat", gripcount=0,
                                 darkcolor="#000", lightcolor="#000", bordercolor="#fff")
            main_theme.configure("W.TEntry", foreground='#000', bordercolor='#000', lightcolor='#000',
                                 fieldbackground='#fff',
                                 selectbackground='#000', selectforeground='#fff')
            main_theme.configure("Horizontal.TScrollbar", gripcount=0, relief="flat",
                                 background="#fff", darkcolor="#fff", lightcolor="#fff",
                                 troughcolor="#fff", bordercolor="#fff", arrowcolor="#000")
            main_theme.map("Horizontal.TScrollbar", background=[('pressed', '!disabled', '#eee'), ('active', '#eee')])
            left_player_music_list.configure(selectbackground="#000", foreground='#000', background='#fff',
                                             relief="flat")
            main_player_frame.configure(background="#fff")
            buttons_player_frame.configure(background="#fff")
            right_player_frame.configure(background="#fff")
            bottom_player_frame.configure(background="#fff")
            top_player_frame.configure(background="#fff")
            settings_frame_third.configure(background="#fff")
            settings_frame_second.configure(background="#fff")
            settings_frame_first.configure(background="#fff")
            settings_bar_frame.configure(background="#fff")
            main_settings_frame.configure(background="#fff")
            settings_frame_fourth.configure(background="#fff")
            main_window.configure(background="#fff")
            settings_frame_fifth.configure(background="#fff")
            settings_frame_sixth.configure(background="#fff")
            left_player_frame.configure(background="#fff")
            bottom_time_frame.configure(background="#fff")
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
            settings_back_button.configure(image=back_img)
            top_player_folder_button.configure(image=folder_img)
            top_player_refresh_button.configure(image=refresh_img)
            third_settings_theme_button.configure(image=toggle_off_img)
            if config["gtr_buffer"]:
                fourth_settings_buffer_button.configure(image=toggle_on_img)
            else:
                fourth_settings_buffer_button.configure(image=toggle_off_img)
            if config["mode"] == "r_n":
                mode_player_mode_button.configure(image=repeat_none_img)
            elif config["mode"] == "r_a":
                mode_player_mode_button.configure(image=repeat_all_img)
            elif config["mode"] == "r_o":
                mode_player_mode_button.configure(image=repeat_one_img)
            if config["continue"]:
                fifth_settings_continue_button.configure(image=toggle_on_img)
            else:
                fifth_settings_continue_button.configure(image=toggle_off_img)
            if config["fade"]:
                sixth_settings_fade_button.configure(image=toggle_on_img)
            else:
                sixth_settings_fade_button.configure(image=toggle_off_img)
        elif config["theme"] == "dark":
            main_theme.configure("W.TLabel", foreground='#fff', background='#000', border='0')

            main_theme.configure("W.Horizontal.TProgressbar", foreground='#000', background='#1e88e5', lightcolor='#000'
                                 , darkcolor='#000', bordercolor='#000', troughcolor='#000')
            main_theme.configure("TButton", relief="flat", background='#000',
                                 font=('Bahnschrift', 11), foreground='#fff')
            main_theme.map("TButton", background=[('pressed', '!disabled', '#000'), ('active', '#111')])
            main_theme.map("TScale", background=[('pressed', '!disabled', '#0d77d4'), ('active', '#0d77d4')])
            main_theme.configure("TScale", troughcolor='#111', background='#1e88e5', relief="flat",
                                 gripcount=0, darkcolor="#1e88e5", lightcolor="#1e88e5", bordercolor="#000")
            main_theme.configure("Horizontal.TScrollbar", gripcount=0, relief="flat", background="#000",
                                 darkcolor="#000", lightcolor="#000", troughcolor="#000", bordercolor="#000",
                                 arrowcolor="#1e88e5")
            main_theme.map("Horizontal.TScrollbar", background=[('pressed', '!disabled', '#111'), ('active', '#111')])
            left_player_music_list.configure(selectbackground="#1e88e5", foreground='#fff', background='#000',
                                             relief="flat")
            main_player_frame.configure(background="#000")
            buttons_player_frame.configure(background="#000")
            right_player_frame.configure(background="#000")
            bottom_player_frame.configure(background="#000")
            top_player_frame.configure(background="#000")
            settings_frame_third.configure(background="#000")
            settings_frame_second.configure(background="#000")
            settings_frame_first.configure(background="#000")
            settings_bar_frame.configure(background="#000")
            main_settings_frame.configure(background="#000")
            settings_frame_fourth.configure(background="#000")
            main_window.configure(background="#000")
            settings_frame_fifth.configure(background="#000")
            settings_frame_sixth.configure(background="#000")
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
            if config["gtr_buffer"]:
                fourth_settings_buffer_button.configure(image=toggle_on_img)
            else:
                fourth_settings_buffer_button.configure(image=toggle_off_img)
            if config["mode"] == "r_n":
                mode_player_mode_button.configure(image=repeat_none_img)
            elif config["mode"] == "r_a":
                mode_player_mode_button.configure(image=repeat_all_img)
            elif config["mode"] == "r_o":
                mode_player_mode_button.configure(image=repeat_one_img)
            if config["continue"]:
                fifth_settings_continue_button.configure(image=toggle_on_img)
            else:
                fifth_settings_continue_button.configure(image=toggle_off_img)
            if config["fade"]:
                sixth_settings_fade_button.configure(image=toggle_on_img)
            else:
                sixth_settings_fade_button.configure(image=toggle_off_img)
        else:
            config["theme"] = "light"
            return False
        return True
    except Exception as e:
        dump(e)
        return False


def debug(char) -> None:
    global config
    if char.keysym == "F12":
        show(main_debug_screen, "main_debug_screen")
        debug_info.set("refresh_time: " + str(config["refresh_time"]) + "\ntheme: "
                       + str(config["theme"]) + "\nversion: " + str(config["version"]) + "\ntransition_duration: "
                       + str(config["transition_duration"]) + "\ngtr_buffer: " + str(config["gtr_buffer"]) + "\nmode: "
                       + str(config["mode"]) + "\ncontinue: " + str(config["continue"]) + "\nfade: "
                       + str(config["fade"]) + "\ndebug: " + str(config["debug"]) + "\nmusic_title: "
                       + str(music_title.get()) + "\nmusic_artist: " + str(music_artist.get())
                       + "\nmusic_position: " + str(music_position.get()) + "\nmusic_total: "
                       + str(music_total.get()) + "\nalbum_name: " + str(album_name.get()) + "\nnum_of_songs: "
                       + str(num_of_songs) + "\ncurrent_song: " + str(current_song) + "\nplay_button_state: "
                       + str(play_button_state))


def apply_settings() -> bool:
    global config
    try:
        first_settings_refresh_scale.set(config["refresh_time"])
        second_settings_duration_scale.set(config["transition_duration"])
        music_position.set("--:--")
        music_total.set("--:--")
        debug_info.set("")
        if config["fade"]:
            main_window.bind("<FocusIn>", fade)
            main_window.bind("<FocusOut>", fade)
        if config["debug"]:
            main_window.bind('<Key>', debug)
            logging.basicConfig(filename=sounder_dir + "\\errors.log", level=logging.DEBUG)
        else:
            logging.basicConfig(filename=sounder_dir + "\\errors.log", level=logging.ERROR)
    except Exception as e:
        dump(e)
        return False
    return True


def init_mixer() -> bool:
    global config
    try:
        if config["gtr_buffer"]:
            mixer.pre_init(frequency=44100, size=16, channels=2, buffer=8192, devicename=None)
        else:
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096, devicename=None)
        mixer.init()
        mixer.music.set_volume(99)
    except Exception as e:
        dump(e)
        return False
    try:
        status_thread = threading.Thread(target=song_stats, )
        status_thread.daemon = True
        status_thread.start()
    except Exception as e:
        dump(e)
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
                        if load_music():
                            start_music()
                            refresh_window()
                            set_song_attrib()
                            show(main_player_frame, "main_player_frame")
    except Exception as e:
        dump(e)


def music(button) -> None:
    global num_of_songs, songs, current_song, play_button_state
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
        refresh_dir()


def set_song_attrib() -> None:
    global songs, current_song, album_img, config
    if bool(songs):
        if os.path.splitext(songs[current_song])[1] == ".mp3":
            time_minutes: int
            time_seconds: int
            total_time: float = MP3(songs[current_song]).info.length
            bottom_player_progress_bar["maximum"] = total_time
            time_minutes, time_seconds = divmod(total_time, 60)
            music_total.set(str(int(time_minutes)) + ":" + str(int(time_seconds)).zfill(2))
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
                    right_player_title_label.configure(font='Bahnschrift 11')
                    music_title.set(str(tags["TIT2"]))
                except:
                    if len(songs[current_song]) > 50:
                        right_player_title_label.configure(font='Bahnschrift 9')
                    else:
                        right_player_title_label.configure(font='Bahnschrift 11')
                    music_title.set(os.path.splitext(songs[current_song])[0])
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
                music_title.set(os.path.splitext(songs[current_song])[0])
                music_artist.set("")
            left_player_music_list.selection_clear(0, END)
            left_player_music_list.select_set(current_song)
            music_position.set("0:00")
            config["last_song"] = songs[current_song]
        else:
            bottom_player_progress_bar["maximum"] = 999999
            album_name.set("")
            music_artist.set("")
            right_player_album_art_label.configure(image=default_album_img)
            if len(songs[current_song]) > 50:
                right_player_title_label.configure(font='Bahnschrift 9')
            else:
                right_player_title_label.configure(font='Bahnschrift 11')
            music_title.set(os.path.splitext(songs[current_song])[0])
            left_player_music_list.selection_clear(0, END)
            left_player_music_list.select_set(current_song)
            music_position.set("0:00")
            music_total.set("")
            config["last_song"] = songs[current_song]


def song_stats() -> None:
    global play_button_state, config
    song_length: float
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
                    bottom_player_progress_bar["value"] = song_length
                    time_minutes, time_seconds = divmod(song_length, 60)
                    music_position.set(str(int(time_minutes)) + ":" + str(int(time_seconds)).zfill(2))
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
        dump(e)


def play_loop() -> None:
    global config, current_song, num_of_songs
    if config["mode"] == "r_n":
        music("forward")
    elif config["mode"] == "r_o":
        music("play")
    elif config["mode"] == "r_a":
        if current_song < num_of_songs:
            music("forward")
        else:
            current_song = 0
            music("play")


def mode_change() -> None:
    global config
    if config["mode"] == "r_n":
        config["mode"] = "r_a"
        mode_player_mode_button.configure(image=repeat_all_img)
    elif config["mode"] == "r_a":
        config["mode"] = "r_o"
        mode_player_mode_button.configure(image=repeat_one_img)
    elif config["mode"] == "r_o":
        config["mode"] = "r_n"
        mode_player_mode_button.configure(image=repeat_none_img)


def show(window, scene) -> bool:
    if scene == "main_settings_frame":
        main_window.title("Sounder3 > Settings")
    elif scene == "main_error_frame":
        main_window.title("Sounder3 Error")
    elif scene == "main_debug_screen":
        main_window.title("Debug screen")
    else:
        main_window.title("Sounder3")
    try:
        window.tkraise()
        return True
    except Exception as e:
        dump(e)
        return False


def close() -> None:
    main_player_frame.destroy()
    save_settings()
    sys.exit()


def restart() -> None:
    global sounder_dir
    save_settings()
    main_player_frame.destroy()
    try:
        os.chdir(sounder_dir)
        os.system("start " + sys.argv[0])
    except:
        pass
    sys.exit()


def change_dir_btn() -> None:
    try:
        if change_dir():
            refresh_dir()
    except:
        pass


def list_box_selector(event=None) -> None:
    music("list")


def set_refresh(value) -> None:
    global config
    config["refresh_time"] = round(float(value), 1)


def set_duration(value) -> None:
    global config
    config["transition_duration"] = round(float(value), 1)


def toggle_theme() -> None:
    global config
    try:
        if config["theme"] == "light":
            config["theme"] = "dark"
        elif config["theme"] == "dark":
            config["theme"] = "light"
        if apply_theme():
            set_song_attrib()
    except Exception as e:
        dump(e)


def toggle_buffer() -> None:
    global config
    try:
        if config["gtr_buffer"]:
            fourth_settings_buffer_button.configure(image=toggle_off_img)
            config["gtr_buffer"] = False
        else:
            fourth_settings_buffer_button.configure(image=toggle_on_img)
            config["gtr_buffer"] = True
    except Exception as e:
        dump(e)


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
        dump(e)


def toggle_fade() -> None:
    global config
    try:
        if config["fade"]:
            sixth_settings_fade_button.configure(image=toggle_off_img)
            config["fade"] = False
            main_window.unbind("<FocusIn>")
            main_window.unbind("<FocusOut>")
        elif not config["fade"]:
            sixth_settings_fade_button.configure(image=toggle_on_img)
            config["fade"] = True
            main_window.bind("<FocusIn>", fade)
            main_window.bind("<FocusOut>", fade)
    except Exception as e:
        dump(e)


def fade(event):
    if str(event.type) == "FocusIn":
        main_window.attributes('-alpha', 1)
    elif str(event.type) == "FocusOut":
        main_window.attributes('-alpha', 0.3)


def changelog():
    global sounder_dir, config
    os.chdir(sounder_dir)
    changelog_window: ClassVar = Toplevel()
    changelog_window.title("Sounder Changelog")
    changelog_window.geometry('300x200+{0}+{1}'.format(main_window.winfo_x() + 250, main_window.winfo_y() + 150))
    changelog_window.iconbitmap(sounder_dir + "\\icon.ico")
    changelog_window.grab_set()
    changelog_window.resizable(width=FALSE, height=FALSE)
    changelog_text: ClassVar = Text(changelog_window, bd=0, cursor="no", takefocus=0, font=('Bahnschrift', 11))
    changelog_text.place(relx=0.02, rely=0, relwidth=1, relheight=1)
    if config["theme"] == "light":
        changelog_text.configure(selectbackground="#fff", selectforeground="#000")
        changelog_window.configure(background="#fff")
    else:
        changelog_text.configure(selectbackground="#000", selectforeground="#fff", background="#000", foreground="#fff")
        changelog_window.configure(background="#000")
    if os.path.isfile('changelog.txt'):
        with open('changelog.txt', 'r') as text:
            for line in text.readlines():
                changelog_text.insert(END, line)
        changelog_text.configure(state=DISABLED)
    changelog_text.insert(END, "Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert "
                               "you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie "
                               "and hurt you")
    try:
        os.chdir(config["path"].rstrip('\n'))
    except Exception as e:
        dump(e)
    changelog_window.mainloop()


# end
# frames
# debug screen
main_debug_screen: ClassVar = Frame(main_window)
main_debug_screen.configure(background="#fff")
label_debug: ClassVar = ttk.Label(main_debug_screen, text="Debug Screen", font='Bahnschrift 14', background='#fff',
                                  foreground='#000', border='0', anchor="center")
panic_button: ClassVar = ttk.Button(main_debug_screen, cursor="hand2", takefocus=False, text="PANIC!",
                                    command=lambda: show(main_error_frame, "main_error_frame"))
restart_button: ClassVar = ttk.Button(main_debug_screen, cursor="hand2", takefocus=False, text="RESTART"
                                      , command=restart)
main_init_button: ClassVar = ttk.Button(main_debug_screen, text="SHOW MAIN INIT FRAME", cursor="hand2", takefocus=False
                                        , command=lambda: show(main_init_frame, "main_init_frame"))
main_settings_button: ClassVar = ttk.Button(main_debug_screen, text="SHOW MAIN SETTINGS FRAME", cursor="hand2",
                                            takefocus=False
                                            , command=lambda: show(main_settings_frame, "main_settings_frame"))

main_player_button: ClassVar = ttk.Button(main_debug_screen, text="SHOW MAIN PLAYER FRAME", cursor="hand2"
                                          , takefocus=False,
                                          command=lambda: show(main_player_frame, "main_player_frame"))
info_label: ClassVar = ttk.Label(main_debug_screen, textvariable=debug_info, font='Consolas 9', background='#fff',
                                 foreground='#000', border='0', anchor="w")
label_debug.place(relx=0.5, rely=0, relwidth=1, relheight=0.1, anchor="n")
panic_button.place(relx=0.5, rely=0.2, relheight=0.08, relwidth=0.3, anchor="n")
restart_button.place(relx=0.5, rely=0.3, relheight=0.08, relwidth=0.3, anchor="n")
main_init_button.place(relx=0.5, rely=0.4, relheight=0.08, relwidth=0.3, anchor="n")
main_settings_button.place(relx=0.5, rely=0.5, relheight=0.08, relwidth=0.3, anchor="n")
main_player_button.place(relx=0.5, rely=0.6, relheight=0.08, relwidth=0.3, anchor="n")
info_label.place(relx=0.005, rely=0.2)
main_debug_screen.place(relx=0.5, rely=0, anchor="n", width=806, height=500)
# end
# main init frame
main_init_frame: ClassVar = Frame(main_window)
main_init_frame.configure(background="#fff")
logo_label: ClassVar = ttk.Label(main_init_frame, image=logo_1_img, font='Bahnschrift 11', background='#fff'
                                 , foreground='#000', border='0')
version_label: ClassVar = ttk.Label(main_init_frame, text="V" + version[0], font='Bahnschrift 11', background='#fff'
                                    , foreground='#000', border='0')
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
                                     font='Bahnschrift 11', text="The application unexpectedly exited!")
error_info_two: ClassVar = ttk.Label(main_error_frame, background='#fff', foreground='#000', border='0',
                                     font='Bahnschrift 11', text="You can find Diagnostic information in the error log")

error_button: ClassVar = ttk.Button(main_error_frame, cursor="hand2", takefocus=False, text="RESTART",
                                    command=restart)
error_version_label: ClassVar = ttk.Label(main_error_frame, text="V" + version, font='Bahnschrift 11'
                                          , background='#fff', foreground='#000', border='6')
error_img_label.place(relx=0.5, rely=0.15, anchor="n")
error_label.place(relx=0.5, rely=0.36, anchor="n")
error_reason_label.place(relx=0.5, rely=0.45, anchor="n")
error_info_one.place(relx=0.5, rely=0.6, anchor="n")
error_info_two.place(relx=0.5, rely=0.64, anchor="n")
error_button.place(relx=0.5, rely=0.76, anchor="n")
error_version_label.place(relx=0.96, rely=0.94, anchor="n")
main_error_frame.place(relx=0.5, rely=0, anchor="n", width=806, height=500)
# end
# settings frame
main_settings_frame: ClassVar = Frame(main_window)

settings_bar_frame: ClassVar = Frame(main_settings_frame)

settings_label: ClassVar = ttk.Label(settings_bar_frame, text="Settings", font='Bahnschrift 15', style="W.TLabel")
settings_back_button: ClassVar = ttk.Button(settings_bar_frame, cursor="hand2", takefocus=False,
                                            command=lambda: show(main_player_frame, "main_player_frame"))
settings_separator: ClassVar = ttk.Separator(settings_bar_frame, orient="horizontal")
settings_label.place(relx=0.005, rely=0.12)
settings_back_button.place(relx=0.9548, rely=0)
settings_separator.place(relx=0, rely=0.95, height=2, relwidth=1)
settings_bar_frame.place(relx=0, rely=0, width=806, height=38)
main_settings_frame.place(relx=0.5, rely=0, anchor="n", relwidth=1, height=500)
# end

# first setting
settings_frame_first: ClassVar = Frame(main_settings_frame)
first_settings_refresh_label: ClassVar = ttk.Label(settings_frame_first, text="Refresh rate", font='Bahnschrift 12',
                                                   style="W.TLabel")
first_settings_refresh_scale: ClassVar = ttk.Scale(settings_frame_first, from_=1, to=10, orient=HORIZONTAL,
                                                   cursor="hand2", command=set_refresh)
first_settings_refresh_label.pack(side=LEFT)
first_settings_refresh_scale.pack(side=RIGHT)
settings_frame_first.place(relx=0.005, rely=0.08, width=300, height=40)
# end
# second setting
settings_frame_second: ClassVar = Frame(main_settings_frame)
second_settings_duration_label: ClassVar = ttk.Label(settings_frame_second, text="Transition duration"
                                                     , font='Bahnschrift 12', style="W.TLabel")
second_settings_duration_scale: ClassVar = ttk.Scale(settings_frame_second, from_=0, to=10, orient=HORIZONTAL
                                                     , cursor="hand2", command=set_duration)
second_settings_duration_label.pack(side=LEFT)
second_settings_duration_scale.pack(side=RIGHT)
settings_frame_second.place(relx=0.005, rely=0.16, width=300, height=40)
# end
# third setting
settings_frame_third: ClassVar = Frame(main_settings_frame)
third_settings_theme_label: ClassVar = ttk.Label(settings_frame_third, text="Dark theme", font='Bahnschrift 11'
                                                 , style="W.TLabel")
third_settings_theme_button: ClassVar = ttk.Button(settings_frame_third, cursor="hand2", takefocus=False
                                                   , command=toggle_theme)
third_settings_theme_label.pack(side=LEFT, padx=(0, 5))
third_settings_theme_button.pack(side=LEFT, padx=(3, 0))
settings_frame_third.place(relx=0.005, rely=0.24, width=300, height=40)
# end
# fourth setting
settings_frame_fourth: ClassVar = Frame(main_settings_frame)
fourth_settings_buffer_label: ClassVar = ttk.Label(settings_frame_fourth, text="Use double buffer"
                                                   , font='Bahnschrift 11', style="W.TLabel")
fourth_settings_buffer_button: ClassVar = ttk.Button(settings_frame_fourth, cursor="hand2", takefocus=False
                                                     , command=toggle_buffer)
fourth_settings_buffer_label.pack(side=LEFT, padx=(0, 5))
fourth_settings_buffer_button.pack(side=LEFT, padx=(3, 0))
settings_frame_fourth.place(relx=0.005, rely=0.32, width=300, height=40)
# end
# fifth setting
settings_frame_fifth: ClassVar = Frame(main_settings_frame)
fifth_settings_continue_label: ClassVar = ttk.Label(settings_frame_fifth, text="Continue where I left off",
                                                    font='Bahnschrift 11', style="W.TLabel")
fifth_settings_continue_button: ClassVar = ttk.Button(settings_frame_fifth, cursor="hand2", takefocus=False,
                                                      command=toggle_continue)
fifth_settings_continue_label.pack(side=LEFT, padx=(0, 5))
fifth_settings_continue_button.pack(side=LEFT, padx=(3, 0))
settings_frame_fifth.place(relx=0.005, rely=0.4, width=300, height=40)
# end
# sixth setting
settings_frame_sixth: ClassVar = Frame(main_settings_frame)
sixth_settings_fade_label: ClassVar = ttk.Label(settings_frame_sixth, text="Fade Sounder while it is not in use",
                                                font='Bahnschrift 11', style="W.TLabel")
sixth_settings_fade_button: ClassVar = ttk.Button(settings_frame_sixth, cursor="hand2", takefocus=False,
                                                  command=toggle_fade)
sixth_settings_fade_label.pack(side=LEFT, padx=(0, 5))
sixth_settings_fade_button.pack(side=LEFT, padx=(3, 0))
settings_frame_sixth.place(relx=0.005, rely=0.48, width=300, height=40)
# end
settings_version_button: ClassVar = ttk.Button(main_settings_frame,
                                               text="V" + version + " Sounder © by Mateusz Perczak",
                                               takefocus=False, command=changelog, cursor="hand2")
settings_version_button.place(relx=0.005, rely=0.925)
# main frame
main_player_frame: ClassVar = Frame(main_window)
main_player_frame.place(relx=0.5, rely=0, anchor="n", width=806, height=500)

# end
# top frame
top_player_frame: ClassVar = Frame(main_player_frame)
top_player_refresh_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                 command=refresh_dir)
top_player_folder_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                command=change_dir_btn)
top_player_path_label: ClassVar = ttk.Label(top_player_frame, width=85, textvariable=path, font='Bahnschrift 11'
                                            , style="W.TLabel")
top_player_settings_button: ClassVar = ttk.Button(top_player_frame, cursor="hand2", takefocus=False,
                                                  command=lambda: show(main_settings_frame, "main_settings_frame"))
top_player_refresh_button.place(relx=0, rely=0)
top_player_folder_button.place(relx=0.046, rely=0)
top_player_path_label.place(relx=0.095, rely=0.17, relwidth=0.9)
top_player_settings_button.place(relx=0.9548, rely=0)
top_player_frame.place(relx=0, rely=0, width=806, height=36)
# end
# bottom_frame
bottom_player_frame: ClassVar = Frame(main_player_frame)
# left frame
left_player_frame: ClassVar = Frame(bottom_player_frame)
left_player_music_scrollbar: ClassVar = ttk.Scrollbar(left_player_frame, orient=HORIZONTAL, cursor="hand2",
                                                      takefocus=False)
left_player_music_list: ClassVar = Listbox(left_player_frame, font='Bahnschrift 11', cursor="hand2"
                                           , bd=0, activestyle="none", takefocus=False, selectmode="SINGLE",
                                           highlightthickness=0, xscrollcommand=left_player_music_scrollbar.set)
left_player_music_scrollbar.configure(command=left_player_music_list.xview)
left_player_music_scrollbar.place(relx=0.005, rely=0.95, relwidth=1)
left_player_music_list.place(relx=0.005, rely=0, relwidth=1, relheight=0.94)
left_player_frame.place(relx=0, rely=0, width=403, relheight=1)
# end
# right frame
right_player_frame = Frame(bottom_player_frame)
right_player_album_label: ClassVar = ttk.Label(right_player_frame, textvariable=album_name, font='Bahnschrift 10'
                                               , style="W.TLabel")
right_player_album_art_label: ClassVar = ttk.Label(right_player_frame, font='Bahnschrift 11',
                                                   style="W.TLabel")
right_player_title_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_title, font='Bahnschrift 11',
                                               style="W.TLabel", wraplength=350)
right_player_artist_label: ClassVar = ttk.Label(right_player_frame, textvariable=music_artist, font='Bahnschrift 10',
                                                style="W.TLabel")
right_player_album_label.place(relx=0.5, rely=0.008, anchor="n")
right_player_album_art_label.place(relx=0.5, rely=0.06, anchor="n")
right_player_title_label.place(relx=0.5, rely=0.55, anchor="n")
right_player_artist_label.place(relx=0.5, rely=0.6, anchor="n")
right_player_frame.place(relx=0.5, rely=0, width=403, relheight=1)
# end
# buttons_frame
buttons_player_frame: ClassVar = Frame(right_player_frame)
buttons_player_previous_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                      command=lambda: music("previous"))
buttons_player_play_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                  command=lambda: music("play"))
buttons_player_forward_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                                     command=lambda: music("forward"))
mode_player_mode_button: ClassVar = ttk.Button(buttons_player_frame, cursor="hand2", takefocus=False,
                                               command=mode_change)
buttons_player_previous_button.place(relx=0.03, rely=0)
buttons_player_play_button.place(relx=0.5, rely=0, anchor="n")
buttons_player_forward_button.place(relx=0.67, rely=0)
mode_player_mode_button.place(relx=0.5, rely=0.54, anchor="n")
buttons_player_frame.place(relx=0.5, rely=0.67, anchor="n", relwidth=0.3, relheight=0.15)
# bottom_time_frame
bottom_time_frame: ClassVar = Frame(right_player_frame)

bottom_player_now_label: ClassVar = ttk.Label(bottom_time_frame, textvariable=music_position, font='Bahnschrift 10',
                                              style="W.TLabel")
bottom_player_progress_bar: ClassVar = ttk.Progressbar(bottom_time_frame, orient=HORIZONTAL, mode="determinate"
                                                       , style="W.Horizontal.TProgressbar")
bottom_player_end_label: ClassVar = ttk.Label(bottom_time_frame, textvariable=music_total, font='Bahnschrift 10',
                                              style="W.TLabel")
bottom_player_now_label.pack(side=LEFT)
bottom_player_progress_bar.pack(side=LEFT, fill=X, expand=True, pady=(2, 0))
bottom_player_end_label.pack(side=RIGHT)
bottom_time_frame.place(relx=0, rely=0.94, relwidth=1, relheight=0.04)
# end
bottom_player_frame.place(relx=0.5, rely=0.09, anchor="n", relwidth=1, height=464)
# end
# main
show(main_init_frame, "main_init_frame")
init_thread = threading.Thread(target=init_player, )
init_thread.daemon = True
init_thread.start()
# end
left_player_music_list.bind("<<ListboxSelect>>", list_box_selector)
main_window.protocol("WM_DELETE_WINDOW", close)
main_window.mainloop()
