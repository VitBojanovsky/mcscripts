import minescript as m
import threading
import logging
import random
import time
from minescript import EventQueue, EventType

logging.basicConfig(level=logging.INFO)

SIDE_DISTANCE = 96.0        
FORWARD_EXTRA_MIN = 3.0       
FORWARD_EXTRA_MAX = 5.0       
ANGLE_TOLERANCE = 2.0
SUDDEN_MOVE_THRESHOLD = 5.0
BLOCK_CHECK_INTERVAL = 0.3
BLOCK_STUCK_THRESHOLD = 0.01
BLOCK_STUCK_COUNT = 3
MONITOR_INTERVAL = 0.05

running = False
stop_event = threading.Event()
pos_lock = threading.Lock()
current_pos = None
start_orientation = None

def human_delay(base=0.03, extra=0.09):
    time.sleep(base + random.uniform(0, extra))

def press_key(key_func):
    human_delay()
    key_func(True)

def release_key(key_func):
    human_delay()
    key_func(False)

def human_wait(base):
    jitter = random.uniform(-0.05, 0.12)
    stop_event.wait(max(0, base + jitter))

def angle_diff(a: float, b: float) -> float:
    d = (a - b + 180.0) % 360.0 - 180.0
    return d

def position_updater():
    global current_pos
    while running and not stop_event.is_set():
        with pos_lock:
            current_pos = m.player_position()
        human_wait(MONITOR_INTERVAL)

def monitor():
    global start_orientation, running
    prev = None
    with pos_lock:
        prev = current_pos
    while running and not stop_event.is_set():
        yaw, pitch = m.player_orientation()
        if start_orientation:
            syaw, spitch = start_orientation
            if abs(angle_diff(yaw, syaw)) > ANGLE_TOLERANCE or abs(angle_diff(pitch, spitch)) > ANGLE_TOLERANCE:
                m.echo("random orientation changed, Stop.")
                running = False
                stop_event.set()
                break
        with pos_lock:
            pos = current_pos
        if pos and prev:
            dx, dy, dz = abs(pos[0]-prev[0]), abs(pos[1]-prev[1]), abs(pos[2]-prev[2])
            if dx > SUDDEN_MOVE_THRESHOLD or dy > SUDDEN_MOVE_THRESHOLD or dz > SUDDEN_MOVE_THRESHOLD:
                m.echo("random movement, Stop.")
                running = False
                stop_event.set()
                break
            prev = pos
        human_wait(MONITOR_INTERVAL)

def check_blocked():
    global running
    stuck = 0
    with pos_lock:
        last = current_pos
    while running and not stop_event.is_set():
        human_wait(BLOCK_CHECK_INTERVAL)
        with pos_lock:
            now = current_pos
        if last and now:
            dx, dy, dz = abs(now[0]-last[0]), abs(now[1]-last[1]), abs(now[2]-last[2])
            if dx < BLOCK_STUCK_THRESHOLD and dy < BLOCK_STUCK_THRESHOLD and dz < BLOCK_STUCK_THRESHOLD:
                stuck += 1
            else:
                stuck = 0
            if stuck >= BLOCK_STUCK_COUNT:
                m.echo("Blocked, Stop")
                running = False
                stop_event.set()
                break
        last = now

def move_side(distance, direction):
    global current_pos
    with pos_lock:
        start = current_pos
    if not start:
        return
    start_x, start_z = start[0], start[2]

    if direction == -1:
        press_key(m.player_press_left)
    else:
        press_key(m.player_press_right)

    while running and not stop_event.is_set():
        with pos_lock:
            pos = current_pos
        if not pos:
            continue
        dx, dz = abs(pos[0]-start_x), abs(pos[2]-start_z)
        if dx >= distance or dz >= distance:
            break
        human_wait(0.05)

    if direction == -1:
        release_key(m.player_press_left)
    else:
        release_key(m.player_press_right)

def move_forward_extra():
    global current_pos
    distance = random.uniform(FORWARD_EXTRA_MIN, FORWARD_EXTRA_MAX)
    with pos_lock:
        start = current_pos
    if not start:
        return
    start_x, start_z = start[0], start[2]

    while running and not stop_event.is_set():
        with pos_lock:
            pos = current_pos
        if not pos:
            continue
        dx, dz = abs(pos[0]-start_x), abs(pos[2]-start_z)
        if dx >= distance or dz >= distance:
            break
        human_wait(0.05)

def farming():
    global running, start_orientation
    running = True
    stop_event.clear()

    start_orientation = m.player_orientation()

    press_key(m.player_press_forward)
    press_key(m.player_press_attack)

    threading.Thread(target=position_updater, daemon=True).start()
    threading.Thread(target=monitor, daemon=True).start()
    threading.Thread(target=check_blocked, daemon=True).start()

    direction = -1 
    while running and not stop_event.is_set():
        move_side(SIDE_DISTANCE, direction)
        move_forward_extra()
        direction *= -1

    release_key(m.player_press_forward)
    release_key(m.player_press_attack)
    m.player_press_left(False)
    m.player_press_right(False)
    m.echo("stopped")

with EventQueue() as event_queue:
    event_queue.register_key_listener()
    m.echo("F6 start / F7 stop")
    while True:
        event = event_queue.get()
        if event.type == EventType.KEY:
            if event.key == 295 and event.action == 1 and not running:
                threading.Thread(target=farming, daemon=True).start()
            elif event.key == 296 and event.action == 1 and running:
                m.echo("Stop")
                stop_event.set()
                running = False