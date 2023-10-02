import time
import math


STRING_COUNT = 25
LETTER_COUNT = 80
TIMEOUT = 0.1
LAND_POSITION = 23
HELICOPTER = [
    '-----≎-----   ⨂',
    '  /¯¯¯¯¯\____/|',
    ' <______/¯¯¯¯¯¯'
]
TRACK = [
    { "x": 80, "y": 0 },
    { "x": 40, "y": 0 },
    { "x": 40, "y": 20 }
]


def generate_frame(symbol):
    frame = []
    for _ in range(STRING_COUNT):
        frame.append(symbol * LETTER_COUNT)
    return frame


def print_frame(frame):
    for s in range(len(frame)):
        print(frame[s])
    time.sleep(TIMEOUT)


def add_land(frame, string_number):
    frame[string_number] = '-' * LETTER_COUNT


def prepare_copter(x, y):
    copter = HELICOPTER.copy()
    height = len(copter)

    width = len(copter[0])
    if y < -1 * height + 1:
            copter = ['']
    elif y < 0:
        for _ in range(-1 * y):
            copter.pop(0)
    elif y > STRING_COUNT - height:
        for _ in range(height - (STRING_COUNT - y)):
            copter.pop(len(copter) - 1)

    height = len(copter)
    if x < -1 * len(copter[0]) + 1:
            copter = ['']
    elif x < 0:
        for i in range(height):
            copter[i] = copter[i][width + x:]
    elif x > LETTER_COUNT - width:
        for i in range(height):
            copter[i] = copter[i][:width + (LETTER_COUNT - width - x)]
    return copter


def add_helicopter(frame, x, y):
    copter = prepare_copter(x, y)
    new_y = 0 if y < 0 else y
    new_x = 0 if x < 0 else x
    for h in range(len(copter)):
        frame[new_y + h] = frame[new_y + h][:new_x] + copter[h] + frame[new_y + h][new_x + len(copter[h]):]


def get_copter_positions(track):
    points = []
    for stage_number in range(len(track) - 1):
        x_range = track[stage_number + 1]["x"] - track[stage_number]["x"]
        y_range = track[stage_number + 1]["y"] - track[stage_number]["y"]
        stage_shift = math.sqrt(x_range * x_range + y_range * y_range)
        frame_count = int(abs(x_range)) if abs(x_range) >= abs(y_range) else int(abs(y_range))
        delta_shift = stage_shift / frame_count
        x_shift = delta_shift * x_range / stage_shift
        y_shift = delta_shift * y_range / stage_shift
        x = track[stage_number]["x"]
        y = track[stage_number]["y"]
        for _ in range(frame_count):
            x += x_shift
            y += y_shift
            points.append({ "x": int(x), "y": int(y) })
    return points

def print_frames(track, land_position):
    track_points = get_copter_positions(track)
    for point_number in range(len(track_points)):
        frame = generate_frame(' ')
        add_land(frame, land_position)
        x = track_points[point_number]["x"]
        y = track_points[point_number]["y"]
        add_helicopter(frame, x, y)
        print_frame(frame)

print_frames(TRACK, LAND_POSITION)
