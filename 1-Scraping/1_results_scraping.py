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
    """Builds a list of links for all athletes taking part in the race"""
    
    # starting time, to keep track of execution time
    t0 = time.time()
    
    # Setting options for selenium
    options = Options()
    options.add_argument('--headless') 
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=options)

    # Scraping the page source containing the list of all athletes and saving it locally
    driver.get(main_url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result-list')))
    html = driver.page_source
    file_object = open('./results.html', "w")
    file_object.write(html)
    file_object.close()

    # Initializing an empty list that will contain all the individual urls    
    results_urls = []
    
    
    # parsing the page source for all individual urls
    parsed_content = BeautifulSoup(html, 'lxml')
    res_list = parsed_content.find("ol", {"class": "result-list"})
    individual_results_list = res_list.findAll("li", {"class": "bold"})
    for result in individual_results_list:
        try:
            href = result.find("a").get("href")
            results_urls.append(href)
        except:
            pass
    
    # Saving the dataset locally to a csv file
    df = pd.DataFrame(result_urls)
    df.to_csv('./result_urls.csv', index=False)
    number_of_links = len(df)
    duration = int(time.time() - t0)
    print(f"process completed in {duration} seconds and generated {number_of_links} listings urls")

    return results_urls

if __name__ == "__main__":
    link = "https://www.grandraid-reunion.com/francais/resultats/?annee=2021&course=GR"
    result_urls = scrape_results_urls(link)
    print(result_urls)
    print(len(result_urls))