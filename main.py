# Copyright (c) [2024] [Devansh Mittal]. All rights reserved.

import yaml
from Team_Stats import TeamClass
from Player_Stats import PlayerClass

main_url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats'

def main():
    
    with open("config.yml", 'r') as file:
        config = yaml.safe_load(file)

    # Determine which table to fetch
    table_type = config.get("table")

    if table_type == "team":
        with TeamClass(config) as TeamObj:
            TeamObj.get_team_stats(main_url)
    else:
        with PlayerClass(config) as PlayerObj:
            PlayerObj.get_player_stats(main_url)

if __name__ == "__main__":
    main()