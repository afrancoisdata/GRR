from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os

import pandas as pd

def scrape_results_urls(main_url):
    """Builds links for all search pages for a given location"""
    results_urls = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=options)

    driver.get(main_url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result-list')))
    # page = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result-list')))
    html = driver.page_source
    # parsed_content = BeautifulSoup(html, 'lxml')

    file_object = open('./results.html', "w")
    file_object.write(html)
    file_object.close()

    # # print(parsed_content.prettify())
    # individual_results_list = parsed_content.findAll("ol", {"class": "result-list"})
    # # print(listings)
    # for listing in individual_results_list:
    #     try:
    #         href = listing.find("a").get("href")
    #         results_urls.append(href)
    #     except:
    #         pass
    return results_urls


# def list_listings_urls(search_url):
#     t0 = time.time()
#     result_urls = scrape_results_urls(search_url)
#     df = pd.DataFrame(result_urls)
#     df.to_csv('./result_urls.csv', index=False)
#     duration = int(time.time() - t0)
#     number_of_links = len(df)
#     print(f"process completed in {duration} seconds and generated {number_of_links} listings urls")
#     return number_of_links


if __name__ == "__main__":
    link = "https://www.grandraid-reunion.com/francais/resultats/?annee=2021&course=GR"
    # print(list_listings_urls(link))
    result_urls = scrape_results_urls(link)