#!venv\Scripts\python.exe

import moviepy.editor as mpy
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from pygifsicle import optimize
from pathlib import Path
import magic
from bitmath import kB,MB
import os

EVENTS = ("moved","created")
BASE_PATH = r'D:\Jordan_Williams\Chrome download\test'
OUTPUT_FOLDER_NAME = "output"
VIDEO_SIZE_LIMIT_MB = 5

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(event.event_type, event.src_path)
        if (event.event_type in EVENTS):
            

            folder_or_file = event.src_path
            poutput = Path(BASE_PATH).joinpath(OUTPUT_FOLDER_NAME)

            pfolder_or_file = Path(folder_or_file)


            if pfolder_or_file.is_file():
                self.wait_for_file(pfolder_or_file)
                

                if self.is_video(str(pfolder_or_file)):

                    if self.get_file_size(str(pfolder_or_file)) <= self.mb_to_bytes(VIDEO_SIZE_LIMIT_MB):
                
                        file_name = pfolder_or_file.stem #get file name of file tht triggered the event
                        output_path_full = poutput.joinpath(file_name + '.gif') # create full path for ouput

                        output_path_full = str(output_path_full)

                        clip = (mpy.VideoFileClip(folder_or_file)).resize(width=1280)
                        clip.write_gif(output_path_full)
                        clip.close()
                        optimize(output_path_full)
                    else:
                        print(f"File size greater than {VIDEO_SIZE_LIMIT_MB} mb")
                        # print("")
                else:
                    print("Not a video")
                    

    def is_video(self,path):
        try:
            mime = magic.Magic(mime=True)
            filename = mime.from_file(path)
            if filename.find('video') != -1:
                return True

            return False
        except PermissionError:
            return True
        except Exception:
            return False
        

    def get_file_size(self,path):
        return Path(path).stat().st_size
    
    def mb_to_bytes(self,mb):
        size_cap = MB(mb)
        size_cap_bytes = size_cap.to_Byte()

        return size_cap_bytes
    
    def wait_for_file(self,path):
        historical_size = -1
        while (historical_size != os.path.getsize(path)):
            historical_size = os.path.getsize(path)
            time.sleep(1)
        print("file copy has now finished")




if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=BASE_PATH, recursive=False)
    observer.start()
    print("running....")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
        print("stopped...")
