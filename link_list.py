import time
import os
from datetime import datetime
import json
from driver import get_driver
from selenium.webdriver.common.by import By


def is_urls_expired():
    try:
        # get the file's modification timestamp
        timestamp = os.path.getmtime('urls/price.json')
        modified_date = datetime.fromtimestamp(timestamp)
        time_difference = datetime.now() - modified_date
        # check if the time difference is greater than week
        return time_difference.days >= 7
    except Exception as e:
        print(e)
        return True


def get_section_urls():
    with get_driver(visible='yes') as driver:
        section_urls = {}
        driver.get('https://multicity.23met.ru/')
        region_chooser = driver.find_element(By.ID, "regionchooser-0")
        region_chooser.click()
        save_button = driver.find_element(
            By.XPATH, "//input[@onclick='citychooser_save_cities_list_for_user()']")
        save_button.click()
        time.sleep(1)
        second_link = driver.find_element(
            By.XPATH, "//ul[@id='header']//li[2]/a")
        section_urls[second_link.text] = second_link.get_attribute("href")
        third_link = driver.find_element(
            By.XPATH, "//ul[@id='header']//li[3]/a")
        section_urls[third_link.text] = third_link.get_attribute("href")
        span_element = driver.find_element(
            By.XPATH, "//span[contains(text(), 'Цветные металлы')]")
        span_element.click()
        submenu_link = driver.find_element(By.CLASS_NAME, 'submenu_ul')
        links = submenu_link.find_elements(By.TAG_NAME, "a")
        for link in links:
            section_urls[link.text] = link.get_attribute("href")
        return section_urls


def create_urls_json(section, url):
    os.makedirs(os.path.dirname('urls/'), exist_ok=True)
    result = {}
    file_name = url.split('/')[3]
    with get_driver() as driver:
        driver.get(url)
        region_chooser = driver.find_element(By.ID, "regionchooser-0")
        region_chooser.click()
        save_button = driver.find_element(
            By.XPATH, "//input[@onclick='citychooser_save_cities_list_for_user()']")
        save_button.click()
        time.sleep(2)
        left_container = driver.find_element(By.CSS_SELECTOR, "ul.tabs")
        links = left_container.find_elements(By.TAG_NAME, "a")
        spans = left_container.find_elements(By.TAG_NAME, "span")
        for span in spans:
            span.click()
        urls = {}
        for link in links:
            link_text = link.text
            print(link_text)
            try:
                link.click()
            except:
                pass
            time.sleep(1)
            current_container = driver.find_element(
                By.CSS_SELECTOR, "div.pane.current")
            current_links = current_container.find_elements(By.TAG_NAME, "a")
            current_links_list = {current_link.text: current_link.get_attribute(
                "href") for current_link in current_links}
            print(current_links_list)
            urls[link_text] = current_links_list
    result[section] = urls
    with open(f"urls/{file_name}.json", "w", encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False)


def create_urls():
    if is_urls_expired():
        print('parsing urls')
        sections = get_section_urls()
        for section, url in sections.items():
            create_urls_json(section, url)
    else:
        print('Urls not expired')
