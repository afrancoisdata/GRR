from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os

import pandas as pd

def scrape_results_urls():
    """Builds links for all search pages for a given location"""
    results_urls=[]
    file_object = open('./results.html', "r")
    parsed_content = BeautifulSoup(file_object, 'lxml')
    # print(parsed_content.prettify())
    # file_object.write(html)
    # file_object.close()

    res_list = parsed_content.find("ol", {"class": "result-list"})
    # print(res_list)
    individual_results_list = res_list.findAll("li", {"class": "bold"})
    for result in individual_results_list:
        try:
            href = result.find("a").get("href")
            results_urls.append(href)
        except:
            pass
    tot=len(results_urls)
    # save_individual_htmls(results_urls[0], 0)
    for i,url in enumerate(results_urls):
        try:
            time.sleep(3)
            save_individual_htmls(url, i)
            print(f'{i}/{tot} scraping done')
        except Exception as e:
            print("ERROR : " + str(e))
            print(f'{i}/{tot} failed')

    return results_urls


def list_individual_urls():
    t0 = time.time()
    result_urls = scrape_results_urls()
    df = pd.DataFrame(result_urls)
    df.to_csv('./result_urls.csv', index=False)
    duration = int(time.time() - t0)
    number_of_links = len(df)
    print(f"process completed in {duration} seconds and generated {number_of_links} listings urls")
    return number_of_links

def save_individual_htmls(url,num):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    # page = WebDriverWait(driver, 10)
    # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tpass')))
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'resume')))

    try:
        file_object = open(f'./results/{num}.html', "w")
    except:
        file_object = open(f'./results/{num}.html', "w", encoding="utf-8")
    html = driver.page_source

    file_object.write(html)
    file_object.close()

if __name__ == "__main__":
    # print(list_listings_urls(link))
    # result_urls = scrape_results_urls(link)
    result_urls = list_individual_urls()
    print(result_urls)