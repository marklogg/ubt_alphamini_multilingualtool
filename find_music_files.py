import os
import shutil

file = open(f"./excels/music_files.txt", "r")
for line in file.readlines():
    start = line.find("file:///")
    end = line.find(".mp3")
    music_file = line[start + 8: end + 4]
    # print(f"{music_file}")
    if os.path.exists(f"build/localTts/{music_file}"):
        if not os.path.exists(f"build/music"):
            os.mkdir("build/music")
        if not os.path.exists(f"build/music/{music_file}"):
            # print(f"move build/localTts/{music_file} to build/music/{music_file}")
            shutil.move(f"build/localTts/{music_file}", f"build/music/{music_file}")
    else:
        print(f"build/localTts/{music_file} no exists.")
