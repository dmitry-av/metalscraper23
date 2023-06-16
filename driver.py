import os
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
from itertools import cycle
from datetime import datetime


def get_proxy_pool(proxylist_url="https://www.proxyscan.io/download?last_check=3800&uptime=50&ping=600&limit=30&type=http,https"):
    try:
        timestamp = os.path.getmtime('proxy-list.txt')
        time_delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(timestamp)
        if time_delta.minutes < 90:
            with open("proxy-list.txt", 'r') as file:
                proxy_file = file.read()
            proxy_list = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', proxy_file)
            proxy_pool = cycle(proxy_list)
            return proxy_pool
        else:
            raise ValueError
    except:
        response = requests.get(proxylist_url)
        if response.status_code == 200:
            with open("proxy-list.txt", "w") as file:
                file.write(response.text)
            proxy_list = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', response.text)
            proxy_pool = cycle(proxy_list)
            return proxy_pool
        else:
            print("Failed to retrieve the text from the URL")


def get_driver(proxypool=None, visible=None):
    chrome_options = webdriver.ChromeOptions()
    if proxypool:
        proxy = next(proxypool)
        chrome_options.add_argument(f'--proxy-server={proxy}')
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    chrome_options.add_argument(f"user-agent={useragent}")
    if not visible:
        chrome_options.add_argument("-headless")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
