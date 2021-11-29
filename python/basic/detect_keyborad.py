import time

import threading as th

KEEP_PRINTING = True


def key_capture_thread():
    global KEEP_PRINTING
    input()
    KEEP_PRINTING = False


def do_stuff():
    th.Thread(target=key_capture_thread, args=(), name="key_capture_thread", daemon=True).start()
    while True:
        print("do something")
        if KEEP_PRINTING:
            print("still print")
        print("do something")
        time.sleep(2)


do_stuff()
