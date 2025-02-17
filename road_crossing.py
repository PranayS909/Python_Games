import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import numpy as np
import sounddevice as sd

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Global variable to store volume level
volume_norm = 0

def audio_callback(indata, frames, time, status):
    global volume_norm
    if status:
        print(status)
    # Calculate volume level (RMS)
    volume_norm = np.linalg.norm(indata) * 10

# Start sound detection
stream = sd.InputStream(callback=audio_callback)
stream.start()

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    # Move player up if volume exceeds threshold
    if volume_norm > 5:
        player.go_up()

    car_manager.create_car()
    car_manager.move_cars()

    # Detect collision with car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    # Detect successful crossing
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()

# Stop the audio stream gracefully
stream.stop()
stream.close()

screen.exitonclick()
