import pyautogui
import subprocess
import time
from parse_demo import parse_demo
import pandas as pd
import obswebsocket # for recording automatically
from obswebsocket import obsws, requests
import threading
import json
import sys
import keyboard # detecting keypresses

def open_cs2():
    steam_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\bin\\win64\\cs2.exe"
    try:
        subprocess.Popen(steam_path)
        time.sleep(20)  # Wait for the game to open
    except FileNotFoundError:
        print("Error: CS2 executable not found! Check the path.")
    except Exception as e:
        print(f"Unexpected error opening CS2: {e}")

def play_demo(demo_name, player_name):
    try:
        # Open the console and play the demo
        pyautogui.press('`')  # Open console
        time.sleep(0.1)
        pyautogui.typewrite(f'playdemo {demo_name}')
        pyautogui.press('enter')
        pyautogui.press('escape')  # Close console
        time.sleep(10)

        # Close the demoui
        pyautogui.press('`')  # Open console
        time.sleep(0.1)
        pyautogui.typewrite('demoui')  # Close the demoUI and follow the player
        pyautogui.press('enter')
        time.sleep(0.01)
        pyautogui.typewrite('volume .15')  # Close the demoUI and follow the player
        pyautogui.press('enter')
        time.sleep(0.01)
        pyautogui.typewrite(f'spec_player {player_name}')  # Close the demoUI and follow the player
        pyautogui.press('enter')
        pyautogui.press('escape')  # Close console
        pyautogui.moveTo(1920, 1080) # move cursor off the screen
    except Exception as e:
        print(f"Error playing demo: {e}")

def skip_to_respawn(player_name, starts, ends, death_tick_round_times):
    def enter_commands(player_name, freeze_end_time):
        """Executes console commands to skip rounds and follow the player."""
        pyautogui.press('shiftright')  # Pause demo
        pyautogui.press('`')  # Open console
        time.sleep(0.1)
        pyautogui.typewrite(f'demo_goto {freeze_end_time}')  # Skip to freeze end time
        pyautogui.press('enter')  # Execute command
        time.sleep(0.01)
        pyautogui.typewrite(f'spec_player {player_name}')  # Follow the player
        pyautogui.press('enter')  # Execute command
        pyautogui.press('escape')  # Close console
        pyautogui.press('shiftright')  # Play demo
        pyautogui.moveTo(1920, 1080)  # Move cursor off the screen

    TICKRATE = 64  # CS2 Tickrate (ticks per second)
    DELAY = 1  # Delay in seconds

    print("\n[INFO] Press 'N' to skip to the next round. On the last round, it will exit to the main menu.")

    # Iterate through rounds
    for i, start in enumerate(starts.tolist()):
        print(f"Jumping to the start of round {i+1}...")

        enter_commands(player_name, starts[i])

        # Check if the player died in this round
        if i+1 in death_tick_round_times['round'].values:
            row_index = death_tick_round_times[death_tick_round_times['round'] == i+1].index[0]
            ticks_since_freeze_time_end = death_tick_round_times.loc[row_index, 'ticks_since_freeze_time_end']
            sleep_time = (ticks_since_freeze_time_end / TICKRATE) + DELAY
        else:
            sleep_time = ((ends[i] - starts[i]) / TICKRATE) + DELAY

        # Wait but allow skipping
        start_time = time.time()
        while time.time() - start_time < sleep_time:
            if keyboard.is_pressed('n'):  # If 'N' is pressed, skip to next round
                if i == len(starts) - 1:  # If it's the last round
                    print("[EXIT] Last round reached. Exiting to the main menu...")
                    time.sleep(0.5)
                    pyautogui.press('`')  # Open console
                    time.sleep(0.1)
                    pyautogui.typewrite('disconnect')  # Exit to the main menu
                    pyautogui.press('enter')
                    pyautogui.press('`')  # Open console
                    return  # Exit function immediately
                else:
                    print(f"[SKIP] Skipping to round {i+2}...")
                    break  # Move to the next round

            time.sleep(0.1)  # Small delay to reduce CPU usage

def close_cs2():
    pyautogui.press('`')  # Open console
    time.sleep(0.1)
    pyautogui.typewrite('quit')  # Exit to the main menu
    pyautogui.press('enter')

# Function to load configuration from a JSON file
def load_config(config_file="config.json"):
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Error: Config file not found. Make sure config.json exists.")
        exit()
    except json.JSONDecodeError:
        print("Error: Config file is not valid JSON. Please check its format.")
        exit()

def obs_connect():
    # Load configuration
    config = load_config()
    
    # Extract OBS credentials
    host = config.get("obs_host", "localhost")
    port = config.get("obs_port", 4455)
    password = config.get("obs_password", "")

    # Connect to OBS WebSocket server
    try:
        ws = obsws(host, port, password)
        ws.connect()
        print("Connected to OBS WebSocket successfully!")
        return ws
    except Exception as e:
        print(f"Error connecting to OBS WebSocket: {e}")
        exit()

def start_rec(ws):
    # Start recording
    ws.call(requests.StartRecording())
    print("Recording started")

def stop_rec(ws):
    ws.call(requests.StopRecording())
    print("Recording stopped")
    # Disconnect from OBS WebSocket server
    ws.disconnect() 

if __name__ == "__main__":
    # Check if the demo name and player name are provided
    if len(sys.argv) < 3:
        print("Usage: python pov_player.py <demo_name> <player_name>")
        sys.exit(1)

    demo_name = sys.argv[1]
    player_name = sys.argv[2]

    # Parse the demo
    starts, ends, death_tick_round_times = parse_demo(demo_name, player_name)

    if starts is None or ends is None or death_tick_round_times is None:
        print("Error: Failed to parse demo.")
        sys.exit(1)
    # Connect to OBS WebSocket Server
    ws = obs_connect() 
    # START RECORDING
    start_rec(ws) 

    # Attempt to parse the demo
    try:
        starts, ends, death_tick_round_times = parse_demo(demo_name, player_name)

        # Check if parsing failed
        if starts is None or ends is None or death_tick_round_times is None:
            raise ValueError("Demo parsing failed. Please check the demo file and player name.")
        
        print("Demo parsed successfully!")
    except ValueError as ve:
        print(f"Error: {ve}")
        exit()
    except Exception as e:
        print(f"Unexpected error while parsing the demo: {e}")
        exit()

    # open cs2
    open_cs2()
    # play the demo
    play_demo(demo_name, player_name)
    # skipping to respawns
    skip_to_respawn(player_name, starts, ends, death_tick_round_times)
    # close cs2
    close_cs2()
    # STOP RECORDING
    stop_rec(ws)
    print("Script finished successfully!")