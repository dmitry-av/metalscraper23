import json
import time
from selenium.webdriver.common.by import By
import pandas as pd
import os

from driver import get_proxy_pool, get_driver
from link_list import create_urls


def parse_section(filename):
    with open(f'urls/{filename}', 'r', encoding='utf-8') as jsonfile:
        subsections = json.load(jsonfile)
    section_name = list(subsections.keys())[0]
    print(f"Section started: {section_name}")
    subfolder = os.path.splitext(filename)[0]
    os.makedirs(os.path.dirname(f'result/{subfolder}/'), exist_ok=True)
    files = [file for file in os.listdir(
        f'result/{subfolder}') if file.endswith('.csv')]
    counter = 0
    driver = get_driver(proxypool=proxy_pool, visible="yes")
    for item_type, sizes in subsections[section_name].items():
        print(f"parsing subsection: {item_type}")
        csv_name = list(sizes.values())[0].split('/')[4] + ".csv"
        if csv_name in files:
            continue
        df_list = []
        for item_size, url in sizes.items():
            while True:
                try:
                    driver.get(url)
                    try:
                        region_chooser = driver.find_element(
                            By.ID, "regionchooser-0")
                        region_chooser.click()
                        save_button = driver.find_element(
                            By.XPATH, "//input[@onclick='citychooser_save_cities_list_for_user()']")
                        save_button.click()
                    except:
                        pass

                    time.sleep(2)
                    table = driver.find_element(By.ID, "table-price")
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    cities = []
                    for row in rows[1:]:
                        firm = row.find_element(
                            By.CLASS_NAME, "td_firm_link_and_tel")
                        try:
                            city = firm.find_element(
                                By.XPATH, ".//b").get_attribute('title')

                        except:
                            city = ""
                        cities.append(city)
                    table = driver.find_element(
                        By.ID, "table-price").get_attribute('outerHTML')
                    pandas_table = pd.read_html(table)[0]
                    se = pd.Series(cities)
                    pandas_table['Город'] = se.values
                    pandas_table['Размер'] = item_size
                    pandas_table['Подраздел'] = item_type
                    pandas_table['Раздел'] = section_name
                    df_list.append(pandas_table)
                    print(f"{item_size} size saved")
                    counter += 1
                    if counter >= 50:
                        driver.quit()
                        driver = get_driver(
                            proxypool=proxy_pool, visible="yes")
                        counter = 0
                    break
                except Exception as e:
                    print(e)
                    driver.quit()
                    driver = get_driver(proxypool=proxy_pool, visible="yes")
                    continue
        result = pd.concat(df_list)
        result.to_csv(f'result/{subfolder}/{csv_name}', encoding='utf-8')
    driver.quit()


def main():
    try:
        # create URLs if not already created
        create_urls()
        json_files = [file for file in os.listdir(
            'urls/') if file.endswith('.json')]

        if len(json_files) == 0:
            print("No JSON files found in 'urls/' directory.")
            return

        for file in json_files:
            parse_section(file)

        print("All sections completed.")

    except Exception as e:
        print("An error occurred while running the application.")
        print(e)


if __name__ == "__main__":
    proxy_pool = get_proxy_pool()
    main()
