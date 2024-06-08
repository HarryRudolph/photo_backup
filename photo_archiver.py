import glob
import os
import datetime
import time
import shutil

files = glob.glob(r'/mnt/drive/buffer/Camera/*.*')

print(len(files))

TODAY = datetime.datetime.now().timestamp()

for file_path in files:
    file_created_time = os.path.getmtime(file_path)
    seconds_since_created = TODAY - file_created_time

    if seconds_since_created > 60*60*24*90: #90 days
        dt = datetime.datetime.fromtimestamp(file_created_time)
        new_path = f"/mnt/drive/Archive/archive/{dt.year}/{dt.month:02}/{dt.day:02}_{os.path.basename(file_path)}"

        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        if not os.path.exists(new_path):
            shutil.copy2(file_path, new_path)
            print(f"Copied to: {os.path.dirname(new_path)}")
            time.sleep(1)
