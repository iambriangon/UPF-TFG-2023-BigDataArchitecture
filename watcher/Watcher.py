import os
import sys
import time


class Watcher:
    def __init__(self, path='./watcher/files', sleep_time=10, callback=None):
        self.path = path
        self.callback = callback
        self.sleep_time = sleep_time

    def monitor(self):
        print("----" * 10)
        print("Monitoring...")
        print("----" * 10)
        new_files = os.listdir(self.path)

        try:
            if new_files:
                print("New files added!")
                print(new_files)
                self.callback(new_files, self.path)
            else:
                print("No new files found!")
        except:
            print("No callback")
            exit(1)

    def watch(self):
        while True:
            self.monitor()
            time.sleep(self.sleep_time)
