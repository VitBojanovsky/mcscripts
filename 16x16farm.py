import minescript as m
import time
import random
import math

FIELD_SIZE = 16
STEP_TIME = 0.20
STRAFE_TIME = 0.25
REALIGN_TOLERANCE = 0.05

def human_delay(a=0.04, b=0.12):
    time.sleep(random.uniform(a, b))

def press(key):
    human_delay()
    key(True)

def release(key):
    human_delay()
    key(False)

def step_forward():
    press(m.player_press_forward)
    time.sleep(STEP_TIME)
    release(m.player_press_forward)

def strafe(direction):
    if direction == -1:
        press(m.player_press_left)
        time.sleep(STRAFE_TIME)
        release(m.player_press_left)
    else:
        press(m.player_press_right)
        time.sleep(STRAFE_TIME)
        release(m.player_press_right)

def farm_block():
    press(m.player_press_attack)
    time.sleep(0.15)
    release(m.player_press_attack)

    human_delay()

    press(m.player_press_use)
    time.sleep(0.1)
    release(m.player_press_use)

def realign_to_x(target_x):
    while True:
        x, y, z = m.player_position()
        diff = target_x - x

        if abs(diff) <= REALIGN_TOLERANCE:
            break

        if diff > 0:
            m.player_press_right(True)
            time.sleep(0.05)
            m.player_press_right(False)
        else:
            m.player_press_left(True)
            time.sleep(0.05)
            m.player_press_left(False)

def farm_16x16():
    start_x, start_y, start_z = m.player_position()
    direction = 1

    for row in range(FIELD_SIZE):

        for col in range(FIELD_SIZE):
            farm_block()
            if col < FIELD_SIZE - 1:
                step_forward()

        if row < FIELD_SIZE - 1:
            strafe(direction)
            step_forward()
            strafe(direction)

            realign_to_x(start_x)

            direction *= -1

    m.echo("Finished aligned 16x16 farm.")

farm_16x16()