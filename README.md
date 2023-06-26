# Application Description

This application is designed to collect data from a website (https://23met.ru/) and retrieve information about prices for various products in different cities. It utilizes web page parsing technique using Selenium Chrome WebDriver.

The application consists of several modules:

## main.py

The main() function is responsible for executing the parsing process. It checks for the presence of JSON files with the list of sub-section URLs and sizes in the 'urls/' directory. The list of URLs is updated if more than 7 days have passed since the last list was obtained.

parse_section() is responsible for parsing a specific section of the website. It takes the file name as input, reads the sub-sections from the JSON file, and iterates over each sub-section. Within each sub-section, it retrieves data for different product sizes and saves them in CSV files.

## driver.py

The get_driver() function creates and returns a Selenium WebDriver object with optional proxy and visibility settings. It uses the Chrome WebDriver, installing it with ChromeDriverManager. If proxy usage is enabled, it selects the next proxy from the pool and adds it to the Chrome WebDriver settings. If 'visible' is not specified, it launches the WebDriver in the background mode.

A pool of proxy addresses is also created, which the application works with.

## link_list.py

This module contains functions related to obtaining and creating a list of URLs. The is_urls_expired() function checks if the 7-day period since the last retrieval of URLs has expired.

The get_section_urls() function retrieves section URLs using the Selenium WebDriver. It opens the website, selects the region, and saves the section URLs in a dictionary.

## Running the Application

Install all the necessary dependencies listed in the requirements.txt file.

Make sure you have Chrome WebDriver installed. If it is not installed, the application will attempt to install it automatically using ChromeDriverManager.

Run the main.py file to execute the parsing process. During execution, several CSV files will be created with price data.
