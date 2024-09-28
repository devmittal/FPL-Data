# Copyright (c) [2024] [Devansh Mittal]. All rights reserved.

from matplotlib import pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from io import StringIO
from pathlib import Path

class BaseClass:
    def __init__(self):
        # Create relevant directories
        self.csv_directory = Path("csv_files")
        self.plots_directory = Path("plot_files")

        if not self.csv_directory.exists():
            self.csv_directory.mkdir(parents=True, exist_ok=True)

        if not self.plots_directory.exists():
            self.plots_directory.mkdir(parents=True, exist_ok=True)

        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = None

        # Specify the path to ChromeDriver
        service = Service('/usr/local/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_param(self, config, key, default_value):
        value = config.get(key, default_value)
        return value if value is not None and value != "" else default_value

    def load_url(self, url):
        self.driver.get(url)

        # Wait for the page to load (adjust time as needed)
        time.sleep(3)  # You might need to increase this if the content loads slowly

    def getTableAndMergeColumns(self, tableName, mergeColumn):
        # Find the table by ID
        table = self.driver.find_element(By.ID, tableName)

        # Get the HTML of the table
        table_html = table.get_attribute('outerHTML')

        html_data = StringIO(table_html)

        # Convert the HTML table into a DataFrame
        df = pd.read_html(html_data)[0]

        if mergeColumn == True:
            df.columns = [
                sub_col if 'Unnamed' in main_col else f'{main_col}_{sub_col}'.strip('_')
                for main_col, sub_col in df.columns.values
                ]

        return df, table
    
    def getUrlFromColumnAndAppendToDf(self, table, column_index, df, tag_name='th', skip_rows=2):
        rows = table.find_elements(By.TAG_NAME, 'tr')

        url_list = []

        for row in rows[skip_rows:]:
            try:
                # Find the specified column (could be either 'th' or 'td')
                columns = row.find_elements(By.TAG_NAME, tag_name)

                if len(columns) > column_index:  # Check if the column exists
                    # Extract the anchor tag's href attribute in the specified column
                    link = columns[column_index].find_element(By.TAG_NAME, 'a').get_attribute('href')
                    url_list.append(link)
                else:
                    # If the column does not exist, append None or an empty string
                    url_list.append(None)

            except NoSuchElementException:
                # If the column or anchor tag is not found, append None
                url_list.append(None)

        # Add the extracted links as a new column to the existing DataFrame
        df[f'url'] = url_list

        return df
    
    def scatterPlot(self, df, xAxis, yAxis, name, outputFileName):
        x = df[xAxis].values
        y = df[yAxis].values
        names = df[name]

        plt.figure(figsize=(10,6))
        plt.scatter(x, y, color='blue', s=25, edgecolor='black')

        for i,name in enumerate(names):
            plt.text(x[i], y[i], name, fontsize=5, ha='left')

        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        pltTitle = xAxis + ' vs ' + yAxis
        plt.title(pltTitle)

        output_path = self.plots_directory / outputFileName
        plt.savefig(output_path)

    def cleanUp(self):
        if self.driver:
            print("Cleaning up the driver...")
            self.driver.quit()

    