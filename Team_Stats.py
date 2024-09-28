# Copyright (c) [2024] [Devansh Mittal]. All rights reserved.

import pandas as pd
from base import BaseClass
from selenium.webdriver.common.by import By
from datetime import datetime

class TeamClass(BaseClass):

    team_for_stats_table = 'stats_squads_standard_for'
    team_against_stats_table = 'stats_squads_standard_against'

    team_match_logs = 'matchlogs_for'

    main_url = ""

    def __init__(self, config):
        super().__init__()
        # Get team table arguments
        team_config = config.get("team_table", {})
        self.mode = super().get_param(team_config, "mode", "for")
        self.teamList = super().get_param(team_config, "team_list", [])
        self.getFixtureEval = super().get_param(team_config, "fixture_eval", False)
        self.numFixtures = super().get_param(team_config, "number_fixtures", 5)
        self.isScatterPlot = super().get_param(team_config, "scatter_plot", True)
        self.xAxis = super().get_param(team_config, "x_axis", "Per 90 Minutes_xG")  # Default is 'Goals'
        self.yAxis = super().get_param(team_config, "y_axis", "Per 90 Minutes_xAG")  # Default is 'Assists'
        self.plotFileName = super().get_param(team_config, "plot_file_name", "Comparing Attributes for PL teams")
        self.sortBy = super().get_param(team_config, "sort_by", "Per 90 Minutes_xG+xAG")
        self.sortByOrder = super().get_param(team_config, "sort_by_order", False)
        self.csvFileName = super().get_param(team_config, "csv_file_name", "team_stats")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csvFileName = self.csvFileName + "_" + timestamp
    
        
    def __enter__(self):
        return self
    
    def get_fixtures_for_team(self, team_url):
        super().load_url(team_url)

        df, table = super().getTableAndMergeColumns(self.team_match_logs, False)

        fixture_list = []

        for index, row in df.iterrows():
            if 'Premier League' in row['Comp'] and pd.isna(row['Result']):
                if row['Venue'] == 'Home':
                    fixture_list.append(row['Opponent'].upper())
                else:
                    fixture_list.append(row['Opponent'].lower())
            
            # Break the loop if x entries are added to the list
            if len(fixture_list) >= self.numFixtures:
                break

        return fixture_list
    

    def fixture_evaluation(self, df_team, df_oppponent):

        for index, row in df_team.iterrows():
            
            fixture_list = self.get_fixtures_for_team(row['url'])

            xg_sum = 0
            xg_p90_sum = 0

            # For each team in fixture list, grab the corresponding xG and xGp90 numbers
            for team in fixture_list:
                for opponent_index, opponent_row in df_oppponent.iterrows():
                    if team.lower() in opponent_row['Squad'].lower():
                        xg_sum += float(opponent_row['Expected_xG'])
                        xg_p90_sum += float(opponent_row['Per 90 Minutes_xG'])
                        break

            # Add these numbers to a new column in the df
            fixture_eval_xg_title = 'Next ' + str(self.numFixtures) + ' Fixtures xG'
            fixture_eval_xgp90_title = 'Next ' + str(self.numFixtures) + ' Fixtures average xGp90'
            fixtures = 'Next ' + str(self.numFixtures) + ' Fixtures'
            df_team.loc[index, fixtures] = ', '.join(fixture_list)
            df_team.loc[index, fixture_eval_xg_title] = round(xg_sum, 2)
            df_team.loc[index, fixture_eval_xgp90_title] = (
                            round(xg_p90_sum / len(fixture_list), 2) if fixture_list else 0
                        )
                
        return df_team  
        

    def get_team_stats(self, main_url):
        self.main_url = main_url
        # Load the main Premier League Stats url
        super().load_url(main_url)

        # Get the DF and table for attacking data and defensive data
        df_for, table_for = super().getTableAndMergeColumns(self.team_for_stats_table, True)
        df_against, table_against = super().getTableAndMergeColumns(self.team_against_stats_table, True)

        # Check if the user wants attacking or defensive data and appropriately copy it to a common name
        if self.mode == "for":
            df_team = df_for
            df_opponent = df_against
            table_team = table_for
        else:
            # Add "vs " to each entry in the teamList since the team name for defensive data contains "vs " in the beginning
            for i in range(len(self.teamList)):
                self.teamList[i] = f"vs {self.teamList[i]}"

            df_team = df_against
            df_opponent = df_for  
            table_team = table_against

        df_team = super().getUrlFromColumnAndAppendToDf(table_team, 0, df_team, 'th', 2)     

        # Convert the columns to be used for x and y axis to integers since all columns are strings
        df_team[self.xAxis] = pd.to_numeric(df_team[self.xAxis], errors='coerce')
        df_team[self.yAxis] = pd.to_numeric(df_team[self.yAxis], errors='coerce')

        # If user has provided a team list, filter out the DF based on this team list
        if self.teamList:
            df_team = df_team[df_team['Squad'].isin(self.teamList)]
            df_team = df_team.reset_index(drop=True)
        
        # Calculate overperformance and add to DF as a new column
        df_team['Overperformance'] = round(pd.to_numeric(df_team['Performance_Gls'], errors='coerce') - pd.to_numeric(df_team['Expected_xG'], errors='coerce'), 3)

        # If the user want future fixture eval data, get the info
        if ( self.getFixtureEval ):
            final_df = self.fixture_evaluation(df_team, df_opponent)
        else:
            final_df = df_team

        # Convert the sortBy column to integer
        final_df[self.sortBy] = pd.to_numeric(final_df[self.sortBy], errors='coerce')
        # Sort based on user choice
        final_df = final_df.sort_values(by=self.sortBy, ascending=self.sortByOrder)

        # Subset of columns to be printed
        columns_of_interest = ['Squad', 'Playing Time_MP', 'Performance_Gls', 'Performance_Ast', 'Expected_xG', 'Expected_xAG', 'Per 90 Minutes_Gls', 'Per 90 Minutes_Ast', 'Per 90 Minutes_xG', 'Per 90 Minutes_xAG', 'Per 90 Minutes_xG+xAG', 'Overperformance' ]
        print(final_df[columns_of_interest])

        # Write to a csv file
        df_to_export = final_df.drop(['url'], axis=1)
        csv_file_path = str(self.csv_directory / self.csvFileName) + '.csv'
        df_to_export.to_csv(csv_file_path, index=False)

        # Scatter plot the data
        if self.isScatterPlot == True:
            super().scatterPlot(final_df, self.xAxis, self.yAxis, "Squad", self.plotFileName)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An exception occurred: {exc_value}")
             
        super().cleanUp() 
        
