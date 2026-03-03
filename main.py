from pynput.mouse import Button, Controller
import time
import random
from pynput.keyboard import Key, Controller as KeyboardController
keyboard = KeyboardController()
mouse = Controller()

def hold_left_mouse_button(duration=None):
    try:
        print("Holding left mouse button...")
        mouse.press(Button.left)
        
        if duration:
            time.sleep(duration)
            mouse.release(Button.left)
            print(f"Released after {duration} seconds")
        else:
            print("Press Ctrl+C to release the button")
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        mouse.release(Button.left)
        print("\nMouse button released")

if __name__ == "__main__":
    time.sleep(15)
    total_time = 0
    x = 0
    while x < 5:
        while total_time < 200:
            mining_duration = random.randint(40, 60)
            total_time += mining_duration
            hold_left_mouse_button(duration=mining_duration)
            cooldown_duration = random.randint(5, 15)
            time.sleep(cooldown_duration)
            total_time += cooldown_duration
        keyboard.press('t')
        time.sleep(0.1)
        keyboard.release('t')
        keyboard.type("/sell")
        keyboard.press(Key.enter)
        time.sleep(0.1)
        keyboard.release(Key.enter)

        mouse.press(Button.left)
        time.sleep(1)
        mouse.release(Button.left)
        x += 1
        total_time = 0