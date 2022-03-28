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
    
    # starting time, to keep track of execution time
    t0 = time.time()
    
    # Retrieve the list of individual URLs
    urls_df=pd.read_csv('./result_urls.csv')
    tot=len(urls_df)

    # creating a list to keep track of failed url scraping
    errors=[]
    
    # scraping the html for each individual athlete
    for i,row in urls_df.iterrows():
        url=row[0]
        try:
            time.sleep(3)
            save_individual_htmls(url, i)
            print(f'{i}/{tot} scraping done')
        except Exception as e:
            print("ERROR : " + str(e))
            print(f'{i}/{tot} failed')
            errors.append(i)

            
    # print useful execution information at the end
    duration = int(time.time() - t0)
    print(f"process completed in {duration} seconds and {len(errors)} urls failed")
    print(errors)

    return errors


def save_individual_htmls(url,num):
   
    # Setting options for selenium
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(options=options)

    # Scraping the URL
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'resume')))

    # Saving the page source locally. A tricky situation here as some results had sepcial caracters 
    # and needed to be utf-8 encoded
    try:
        file_object = open(f'./results/{num}.html', "w")
    except:
        file_object = open(f'./results/{num}.html', "w", encoding="utf-8")
    html = driver.page_source
    file_object.write(html)
    file_object.close()
    
    return

if __name__ == "__main__":
    result_urls = scrape_results_urls()