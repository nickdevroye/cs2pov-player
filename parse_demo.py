from awpy import Demo

def parse_demo(demo_name,player_name):
    # demo path
    path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo\\"

    # parse demo
    dem = Demo(path+demo_name)

    # df of kills data
    df = dem.kills

    # start ticks
    starts = dem.rounds['freeze_end']

    # end ticks
    ends = dem.rounds['end']

    # filtered df of when player dies
    df_filtered = df.loc[df['victim_name']==player_name]

    # filter only useful columns
    death_tick_round_time = df_filtered[['tick', 'round', 'ticks_since_freeze_time_end']]

    # players total deaths in the game
    #total_deaths=len(death_tick_round_time['round'])

    return starts, ends, death_tick_round_time