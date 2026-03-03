import random
import time
import minescript
from minescript import *
import threading

stop_farming = False

def listen_for_exit():
    global stop_farming
    try:
        import keyboard
        while not stop_farming:
            if keyboard.is_pressed('o'):
                stop_farming = True
                minescript.echo("Exit key pressed - stopping")
                break
            time.sleep(0.1)
    except ImportError:
        minescript.echo("keyboard module not available - no exit key")

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





# Start exit key listener in background
listener_thread = threading.Thread(target=listen_for_exit, daemon=True)
listener_thread.start()

while not stop_farming:
    farming_chunk()
    minescript.echo("Chunk farmed")
    time.sleep(10)

minescript.echo("Farming stopped")