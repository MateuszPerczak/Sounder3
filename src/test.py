import json
import os
import shutil

OUTPUT_PATH = os.path.normpath(os.path.expandvars(os.path.expanduser(r"~/Desktop/MC_Sounds/")))

MC_ASSETS = os.path.expandvars(r"%APPDATA%/.minecraft/assets")

MC_VERSION = "1.16"

MC_OBJECT_INDEX = f"{MC_ASSETS}/indexes/{MC_VERSION}.json"
MC_OBJECTS_PATH = f"{MC_ASSETS}/objects"
MC_SOUNDS = r"minecraft/sounds/"

with open(MC_OBJECT_INDEX, "r") as read_file:
    data = json.load(read_file)
    sounds = {k[len(MC_SOUNDS):]: v["hash"] for (k, v) in data["objects"].items() if k.startswith(MC_SOUNDS)}
    for fpath, fhash in sounds.items():
        src_fpath = os.path.normpath(f"{MC_OBJECTS_PATH}/{fhash[:2]}/{fhash}")
        dest_fpath = os.path.normpath(f"{OUTPUT_PATH}/sounds/{fpath}")
        print(f"copying {src_fpath} --> {dest_fpath}")
        os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
        shutil.copyfile(src_fpath, dest_fpath)
