import glob
import os
import datetime
import time
import shutil
import exiftool

files = glob.glob(r'/mnt/drive/buffer/Camera/*.*')

print(len(files))

TODAY = datetime.datetime.now().timestamp()

for file_path in files:
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(file_path)[0]
        file_created_time = None
        if "EXIF:DateTimeOriginal" in metadata.keys():
            file_created_time = metadata["EXIF:DateTimeOriginal"]
        elif "QuickTime:CreateDate" in metadata.keys():
            file_created_time = metadata["QuickTime:CreateDate"]
        else:
            print(f"No creation date for file: {file_path}")

    file_created_time = datetime.datetime.strptime(file_created_time, "%Y:%m:%d %H:%M:%S")    
    seconds_since_created = TODAY - file_created_time

    if seconds_since_created > 60*60*24*90: #90 days
        dt = datetime.datetime.fromtimestamp(file_created_time)
        new_path = f"/mnt/drive/Archive/archive/{dt.year}/{dt.month:02}/{dt.day:02}_{os.path.basename(file_path)}"

        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        if not os.path.exists(new_path):
            shutil.copy2(file_path, new_path)
            print(f"Copied to: {os.path.dirname(new_path)}")
            time.sleep(1)
