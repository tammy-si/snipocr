from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from dotenv import load_dotenv
import time
import re
import os
from PIL import Image
import pytesseract
import subprocess

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if re.search(r'(?<!\.)Screenshot.*\.png$', event.src_path):
            text = pytesseract.image_to_string(os.path.normpath(event.src_path))
            write_to_clilpboard(text)

def write_to_clilpboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def main():
    load_dotenv()
    pytesseract.pytesseract.tesseract_cmd=os.path.normpath(os.getenv("TESSERACT_PATH"))
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, f"/Users/{os.getenv("USERNAME")}/Desktop", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()    

main()
