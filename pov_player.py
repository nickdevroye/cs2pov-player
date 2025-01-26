import pyautogui
import subprocess
import time
from parse_demo import parse_demo
import pandas as pd
import obswebsocket # for recording automatically
from obswebsocket import obsws, requests

def open_cs2():
    steam_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\bin\\win64\\cs2.exe"
    try:
        subprocess.Popen(steam_path)
        time.sleep(10)  # Wait for the game to open
    except Exception as e:
        print(f"Error opening CS2: {e}")

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
    # console commands when skipping
    def enter_commands(player_name,freeze_end_time):
        pyautogui.press('shiftright')  # pause demo
        pyautogui.press('`')  # Open console
        time.sleep(0.1)
        pyautogui.typewrite(f'demo_goto {freeze_end_time}') # Skip to the freeze end time
        pyautogui.press('enter') # Execute the command
        time.sleep(0.01)
        pyautogui.typewrite(f'spec_player {player_name}') # Follow the player
        pyautogui.press('enter') # Execute the command
        pyautogui.press('escape')  # Close console
        pyautogui.press('shiftright')  # play demo
        pyautogui.moveTo(1920, 1080) # move cursor off the screen
    
    TICKRATE =  64 # IN TICKS PER SECOND
    DELAY = 1 # IN SECONDS
    
    print(death_tick_round_times['round'].values)
    # Script logic
    for i, start in enumerate(starts.tolist()):
        print(f'Skipped to the start of round {i+1} started')
        enter_commands(player_name,starts[i])

        # IF PLAYER DIES
        if i+1 in death_tick_round_times['round'].values:
            # Get the index of the row for the round of death
            row_index = death_tick_round_times[death_tick_round_times['round']==i+1].index[0]
            # Get the ticks_since_freeze_time_end value from the column in the same row
            ticks_since_freeze_time_end = death_tick_round_times.loc[row_index,'ticks_since_freeze_time_end']
            # use ticks_since_freeze_time_end to calculate sleep_time
            sleep_time = ( ticks_since_freeze_time_end / TICKRATE) + DELAY
            time.sleep(sleep_time)

        # ELSE PLAYER LIVED
        else:
            sleep_time = ( (ends[i]-starts[i]) / TICKRATE) + DELAY
            time.sleep(sleep_time)

def close_cs2():
    pyautogui.hotkey('alt', 'f4')

def obs_connect():
    # Replace with your OBS WebSocket server details
    host = "192.168.1.206"
    port = 4455
    password = "TMhEIwLqry1qMpwV"

    # Connect to OBS WebSocket server
    ws = obsws(host, port, password)
    ws.connect()

    return ws

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
    # Connect to OBS WebSocket Server
    ws = obs_connect() 
    # START RECORDING
    start_rec(ws) 
    # Use only the demo name
    demo_name = "astralis-vs-wildcard-m1-inferno.dem"  
    # Name of the player to follow
    player_name = "dev1ce"  
    # parse the demo and clean the data
    starts, ends, death_tick_round_times = parse_demo(demo_name,player_name)
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