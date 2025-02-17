import tkinter as tk
import subprocess
import os

# Function to run a game file
def run_game(game_file):
    try:
        subprocess.Popen(["python", game_file])
    except Exception as e:
        print(f"Error running {game_file}: {e}")

# Create the main window
root = tk.Tk()
root.title("Game Launcher")
root.geometry("400x300")
root.configure(bg="lightblue")

# Label
title_label = tk.Label(
    root, text="Choose a Game to Play", font=("Arial", 16), bg="lightblue", fg="darkblue"
)
title_label.pack(pady=20)

# Buttons for games
games = {
    "Balls Game": r"C:\Python Learning\GAMES\collect_balls.py",
    "Flappy Ball": r"C:\Python Learning\GAMES\flappybird.py",
    "Turtle Crossing": r"C:\Python Learning\GAMES\road_crossing.py",
}

for game_name, game_file in games.items():
    # Ensure the game file exists
    if not os.path.exists(game_file):
        with open(game_file, "w") as f:
            f.write("# Placeholder file for " + game_name + "\nprint('Launching " + game_name + "')\n")

    btn = tk.Button(
        root,
        text=game_name,
        font=("Arial", 14),
        bg="green",
        fg="white",
        command=lambda g=game_file: run_game(g),
        width=20,
        height=2,
    )
    btn.pack(pady=10)

# Exit button
exit_btn = tk.Button(
    root,
    text="Exit",
    font=("Arial", 14),
    bg="red",
    fg="white",
    command=root.quit,
    width=20,
    height=2,
)
exit_btn.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
