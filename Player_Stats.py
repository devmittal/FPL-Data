# Copyright (c) [2024] [Devansh Mittal]. All rights reserved.

import pandas as pd
from base import BaseClass
import yaml
from datetime import datetime

class PlayerClass(BaseClass):

    def __init__(self, config):
        super().__init__()
        # Get team table arguments
        player_config = config.get("player_table", {})
        self.minThres = super().get_param(player_config, "min_minutes", 0)  # Default is 0 minutes
        self.xgiThres = super().get_param(player_config, "min_xGi", 0)  # Default is 0 xGi
        self.playerPosition = super().get_param(player_config, "position", "")
        self.playerList = super().get_param(player_config, "player_list", [])
        self.isScatterPlot = super().get_param(player_config, "scatter_plot", True)
        self.xAxis = super().get_param(player_config, "x_axis", "Per 90 Minutes_xG")  # Default is 'xG'
        self.yAxis = super().get_param(player_config, "y_axis", "Per 90 Minutes_xAG")  # Default is 'xA'
        self.plotFileName = super().get_param(player_config, "plot_file_name", "Comparing Attributes for PL Players")
        self.sortBy = super().get_param(player_config, "sort_by", "Per 90 Minutes_xG+xAG")
        self.sortByOrder = super().get_param(player_config, "sort_by_order", False)
        self.csvFileName = super().get_param(player_config, "csv_file_name", "team_stats")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csvFileName = self.csvFileName + "_" + timestamp

        print(self.csvFileName)


    def __enter__(self):
        return self

    def get_player_stats(self, main_url):

        super().load_url(main_url)
        
        df, table = super().getTableAndMergeColumns('stats_standard', True)

        df['Playing Time_Min'] = pd.to_numeric(df['Playing Time_Min'], errors='coerce')
        df['Per 90 Minutes_xG+xAG'] = pd.to_numeric(df['Per 90 Minutes_xG+xAG'], errors='coerce')
        df[self.xAxis] = pd.to_numeric(df[self.xAxis], errors='coerce')
        df[self.yAxis] = pd.to_numeric(df[self.yAxis], errors='coerce')

        if not self.playerList:
            filteredPlayers = df[df['Playing Time_Min'] > self.minThres]

            filteredPlayers = filteredPlayers[filteredPlayers['Per 90 Minutes_xG+xAG'] >= self.xgiThres]

            filteredPlayers = filteredPlayers[filteredPlayers['Pos'].str.contains(self.playerPosition, case=False, na=False)]

            final_df = filteredPlayers.reset_index(drop=True)
        else:
            filteredPlayers = df[df['Player'].isin(self.playerList)]
            final_df = filteredPlayers.reset_index(drop=True)

        final_df['Overperformance'] = round(pd.to_numeric(final_df['Performance_Gls'], errors='coerce') - pd.to_numeric(final_df['Expected_xG'], errors='coerce'), 3)

        final_df[self.sortBy] = pd.to_numeric(final_df[self.sortBy], errors='coerce')
        final_df = final_df.sort_values(by=self.sortBy, ascending=self.sortByOrder)

        columns_of_interest = ['Player', 'Playing Time_MP', 'Playing Time_Min', 'Performance_Gls', 'Performance_Ast', 'Expected_xG', 'Expected_xAG', 'Per 90 Minutes_Gls', 'Per 90 Minutes_Ast', 'Per 90 Minutes_xG', 'Per 90 Minutes_xAG', 'Per 90 Minutes_xG+xAG', 'Overperformance']
        print(final_df[columns_of_interest])

        csv_file_path = str(self.csv_directory / self.csvFileName) + '.csv'
        final_df.to_csv(csv_file_path, index=False)

        if self.isScatterPlot == True:
            super().scatterPlot(final_df, self.xAxis, self.yAxis, "Player", self.plotFileName)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An exception occurred: {exc_value}")

        super().cleanUp()