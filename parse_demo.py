from awpy import Demo
import os

def parse_demo(demo_name, player_name):
    try:
        # Define demo path
        path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\"
        full_path = os.path.join(path, demo_name)

        # Check if file exists
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Demo file not found: {full_path}")

        # Parse the demo
        dem = Demo(full_path)

        # Extract data
        df = dem.kills
        starts = dem.rounds.get('freeze_end', [])
        ends = dem.rounds.get('end', [])

        # Filter player's death data
        df_filtered = df.loc[df['victim_name'] == player_name]
        death_tick_round_time = df_filtered[['tick', 'round', 'ticks_since_freeze_time_end']]

        # Ensure valid data
        if starts is None or ends is None or death_tick_round_time.empty:
            raise ValueError("Parsing failed: No valid data found in the demo file.")

        return starts, ends, death_tick_round_time
    
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except Exception as e:
        print(f"Unexpected error while parsing demo: {e}")

    # Return None on failure
    return None, None, None

if __name__ == '__main__':
    # Test the function
    # Use only the demo name
    demo_name = "astralis-vs-wildcard-m1-inferno.dem"  
    # Name of the player to follow
    player_name = "dev1ce"  
    starts, ends, death_tick_round_times = parse_demo(demo_name, player_name)
    if starts is not None:
        print(f"Starts: {starts}")
        print(f"Ends: {ends}")
        print(f"Death data: {death_tick_round_times}")
    else:
        print("Parsing failed.")