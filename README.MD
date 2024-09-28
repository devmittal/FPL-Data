# FPL Data

An easy way to retrieve FPL relevant for PL teams and players. All data is fetched from fbref.com. The following features are supported at the moment

1. Fetch PL teams data (Fetched from the [Squad Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table)

    1. Can fetch attacking or defensive stats
    2. Can filter by specifying a list of teams
    3. Can get cumulative xG and average xG per 90 data for the next x number of PL fixtures which is specified by the user. (Will get defensive stats of opponents if attacking stats requested for team and vice versa)
    4. Ability to create a scatter plot with user specified x-axis and y-axis and plot name.
    5. User can sort the resultant table based on their column of choice
    6. Table is exported to csv file where file name is specified by the user

2.  Fetch PL players data (Fetched from the [Player Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table)

    1. Optional filter based on min number of minutes played
    2. Optional filter based on min xGI
    3. Optional filter based on player position
    4. Can filter by specifying a list of players
    5. Ability to create a scatter plot with user specified x-axis and y-axis and plot name.
    6. User can sort the resultant table based on their column of choice
    7. Table is exported to csv file where file name is specified by the user

## Instructions

1. Download the [executable]([url](https://github.com/devmittal/FPL-Data/blob/master/FPL-Data)) and the [config]([url](https://github.com/devmittal/FPL-Data/blob/master/config.yml)) file
2. Update the config file and specify the parameters that you are interested to fetch (Details about the config file is below)
3. Run the executable in your command line from the folder where you downloaded it as follows
   
   ```./FPL-Data```

## Config File

table: "player" or "team"

### team_table

**mode:** "for" - attacking stats; "against" - defensive stats

**team_list:** Comma separated team names. Team name have to match the names specified in the "Squad" column of the [Squad Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table

**fixture_eval:** True if you want to get future fixtures data for each team; otherwise False

**number_fixtures:** Number of fixtures for which you want future data

**scatter_plot:** False if you don't want a scatter plot; True otherwise

**x_axis:** Column name from the [Squad Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table which you wish to plot on the x axis. Note: Combine the main column name and sub column name with an "_". Eg. if you wish to plot the xGp90 you would specify "Per 90 Minutes_xG+xAG". If it does not have a main column name, just specify the sub column name

**y_axis:** Column name from the [Squad Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table which you wish to plot on the y axis. Note: Combine the main column name and sub column name with an "_". Eg. if you wish to plot the xGp90 you would specify "Per 90 Minutes_xG+xAG". If it does not have a main column name, just specify the sub column name

**plot_file_name:** File name for the scatter plot

**sort_by:** Which column you wish to sort the table by. Specify column name from the [Squad Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table Note: Combine the main column name and sub column name with an "_". Eg. if you wish to plot the xGp90 you would specify "Per 90 Minutes_xG+xAG". If it does not have a main column name, just specify the sub column name

**sort_by_order:** False - descending; True - ascending

**csv_file_name:** File name for the output csv file

### player_table

**min_minutes:** Optional filter based on minimum number of minutes played

**min_xGi:** Optional filter based on minimum xGI

**position:** Optional filter based on position of player (DF, MF, FW, GK)

**player_list:** Comma separated player list. Player name has to match the player name in the "Player" column of the [Player Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table

**scatter_plot:** False if you don't want a scatter plot; True otherwise

**x_axis:** Column name from the [Player Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table which you wish to plot on the x axis. Note: Combine the main column name and sub column name with an "_". Eg. if you wish to plot the xGp90 you would specify "Per 90 Minutes_xG+xAG". If it does not have a main column name, just specify the sub column name

**y_axis:** Column name from the [Player Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table which you wish to plot on the y axis. Note: Combine the main column name and sub column name with an "_". Eg. if you wish to plot the xGp90 you would specify "Per 90 Minutes_xG+xAG". If it does not have a main column name, just specify the sub column name

**plot_file_name:** File name for the scatter plot

**sort_by:** Which column you wish to sort the table by. Specify column name from the [Player Standard Stats]([url](https://fbref.com/en/comps/9/stats/Premier-League-Stats)) table Note: Combine the main column name and sub column name with an "_". Eg. if you wish to plot the xGp90 you would specify "Per 90 Minutes_xG+xAG". If it does not have a main column name, just specify the sub column name

**sort_by_order:** False - descending; True - ascending

**csv_file_name:** File name for the output csv file


## License 

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for more details.

**Summary of the License**

The GNU General Public License (GPL) is a free software license that guarantees end users the freedom to run, study, share, and modify the software. This license ensures that the software remains free for all its users.
 
**Usage**

You can freely use, modify, and distribute this project, as long as you adhere to the terms of the GPL.