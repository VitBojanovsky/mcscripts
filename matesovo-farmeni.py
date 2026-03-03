import random
import time
import minescript
from minescript import *
import threading

running = False
stop_event = threading.Event()

def straight_farm():
         for i in range(0,16):
            minescript.press_key_bind("key.attack", True)
            minescript.echo("ATTACK TRUE")
            time.sleep(0.05)
            minescript.press_key_bind("key.attack", False)
            minescript.echo("ATTACK FALSE")
            time.sleep(0.05)
            minescript.press_key_bind("key.use", True)
            minescript.echo("USE TRUE")
            time.sleep(0.05)
            minescript.press_key_bind("key.use", False)
            minescript.echo("USE FALSE")
            time.sleep(0.05)
            minescript.player_press_forward(True)
            minescript.echo("WALK")
            time.sleep(0.232)
            minescript.player_press_forward(False)

def farming_chunk():
    a = minescript.player_orientation()
    minescript.echo(a)
    x,y,z = 0,0,0
    minescript.player_set_orientation(270,90)
    for i in range(0,8):
        straight_farm()
        minescript.player_set_orientation(360,90)
        minescript.player_press_forward(True)
        time.sleep(0.2316)
        minescript.player_press_forward(False)
        minescript.player_set_orientation(90,90)
        straight_farm()
        minescript.player_set_orientation(0,90)
        minescript.player_press_forward(True)
        time.sleep(0.2316)
        minescript.player_press_forward(False)
        minescript.player_set_orientation(270,90)





def farming():
    global running
    while not stop_event.is_set():
        farming_chunk()
        minescript.echo("Chunk farmed")
        time.sleep(10)
    running = False

with EventQueue() as event_queue:
    event_queue.register_key_listener()
    minescript.echo("F6 start / F7 stop")
    while True:
        event = event_queue.get()
        if event.type == EventType.KEY:
            if event.key == 295 and event.action == 1 and not running:  # F6 start
                minescript.echo("Starting farming...")
                stop_event.clear()
                running = True
                threading.Thread(target=farming, daemon=True).start()
            elif event.key == 296 and event.action == 1 and running:  # F7 stop
                minescript.echo("Stopping farming...")
                stop_event.set()
                running = False