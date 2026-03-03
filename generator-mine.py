import minescript
import time
import random

def hold_left_mouse_button(duration=None):
    try:
        minescript.echo("Holding left mouse button...")
        minescript.player_press_attack(True)
        
        if duration:
            time.sleep(duration)
            minescript.player_press_attack(False)
            minescript.echo(f"Released after {duration} seconds")
        else:
            minescript.echo("Press Ctrl+C to release the button")
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        minescript.player_press_attack(False)
        minescript.echo("Mouse button released")

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
        
        # Send /sell command using chat
        minescript.chat("/sell")
        time.sleep(1)
        
        # Click the mouse once
        minescript.player_press_attack(True)
        time.sleep(0.2)
        minescript.player_press_attack(False)
        
        x += 1
        total_time = 0
