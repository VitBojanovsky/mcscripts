import minescript as m
import time
import random

FIELD_SIZE = 16
STEP_DELAY = 0.1  # simple delay between steps

def human_delay():
    time.sleep(random.uniform(STEP_DELAY, STEP_DELAY + 0.1))

def farm_block():
    # Harvest
    m.player_press_attack(True)
    time.sleep(0.15)
    m.player_press_attack(False)

    human_delay()

    # Replant
    m.player_press_use(True)
    time.sleep(0.1)
    m.player_press_use(False)

    human_delay()

def step_forward():
    m.player_press_forward(True)
    time.sleep(0.2)
    m.player_press_forward(False)
    human_delay()

def strafe(direction):
    if direction == -1:
        m.player_press_left(True)
        time.sleep(0.25)
        m.player_press_left(False)
    else:
        m.player_press_right(True)
        time.sleep(0.25)
        m.player_press_right(False)
    human_delay()

def farm_16x16():
    direction = 1  # 1 = right, -1 = left

    for row in range(FIELD_SIZE):
        for col in range(FIELD_SIZE):
            farm_block()
            if col < FIELD_SIZE - 1:
                step_forward()

        if row < FIELD_SIZE - 1:
            strafe(direction)
            step_forward()
            strafe(direction)
            direction *= -1  # reverse direction for zig-zag

    m.echo("Finished 16x16 farm.")

farm_16x16()