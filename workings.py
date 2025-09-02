from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import re
import time
import re
from bs4 import BeautifulSoup
import requests
import webbrowser
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

input_url = "https://www.domain.com.au/17-2-12-temple-street-ashwood-vic-3147-2020228728"
# TIMEOUT = 20

# #st.title("Test Selenium")

# firefoxOptions = Options()
# firefoxOptions.add_argument("--headless")
# service = Service(GeckoDriverManager().install())
# driver = webdriver.Firefox(
#     options=firefoxOptions,
#     service=service,
# )
# driver.get(input_url)

def propHistory(input_url):
    ph_url = re.sub(r'-(\d+)$', '', input_url)           # remove the trailing -digits
    ph_url = ph_url.replace(".com.au/", ".com.au/property-profile/")
    print(ph_url)

    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    )
    driver.get(ph_url)
    time.sleep(1)
    button = driver.find_element(By.XPATH, "//button[text()='View more results']")
    button.click()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(4)
    driver.quit()

    items = []
    list_element = soup.find('ul', {'class': 'css-m3i618'})

    for li in list_element.find_all("li", {"class": "css-16ezjtx"}):
        category = li.find('div', {'data-testid': 'fe-co-property-timeline-card-category'}).get_text(strip=True)
        price = li.find('span', {'data-testid': 'fe-co-property-timeline-card-heading'}).get_text(strip=True)
        period = li.find('span', {'data-testid': 'fe-co-property-timeline-card-heading'}).find_next('span').get_text(strip=True)
        month = li.find('div', {'class': 'css-vajoca'}).get_text(strip=True).upper()
        year = li.find('div', {'class': 'css-1qi20sy'}).get_text(strip=True)

        items.append({
            "category": category,
            "price": price,
            "period": period,
            "month": month,
            "year": year
        })

    df = pd.DataFrame(items)
    print(df)

    return df
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # print("Page title:", soup.title.string if soup.title else "No title")
    # print("First 200 chars:", str(soup)[:200])
    # # Look for ANY buttons
    # buttons = soup.find_all('button')
    # print(f"Found {len(buttons)} buttons:")
    # for i, btn in enumerate(buttons):  # Show first 5 buttons
    #     print(f"Button {i}: {btn}")
    #print(soup)
    # time.sleep(1)
    # try:
    #     #button = driver.find_element(By.XPATH, "//button[text()='View more results']")
    #     #button = WebDriverWait(driver, timeout).until(
    #     #            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='View more results']"))
    #     #        )
    #     button = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='css-1l0j5hd' and normalize-space()='View more results']")))
    #     print("Found button with partial text match")
    # except TimeoutException:
    #     print("No button with 'View more' text found")
        
    #     # Try finding by class only
    #     try:
    #         button = WebDriverWait(driver, timeout).until(
    #             EC.element_to_be_clickable((By.CLASS_NAME, "css-1l0j5hd"))
    #         )
    #         print("Found button by class name")
    #     except TimeoutException:
    #         print("No button with that class found either")
    # button.click()
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # print(f"First 10 chars of html: {str(soup)[:10]}")
    
    # time.sleep(4)
    # driver.quit()

    # items = []
    # list_element = soup.find('ul', {'class': 'css-m3i618'})

    # for li in list_element.find_all("li", {"class": "css-16ezjtx"}):
    #     category = li.find('div', {'data-testid': 'fe-co-property-timeline-card-category'}).get_text(strip=True)
    #     price = li.find('span', {'data-testid': 'fe-co-property-timeline-card-heading'}).get_text(strip=True)
    #     period = li.find('span', {'data-testid': 'fe-co-property-timeline-card-heading'}).find_next('span').get_text(strip=True)
    #     month = li.find('div', {'class': 'css-vajoca'}).get_text(strip=True).upper()
    #     year = li.find('div', {'class': 'css-1qi20sy'}).get_text(strip=True)

    #     items.append({
    #         "category": category,
    #         "price": price,
    #         "period": period,
    #         "month": month,
    #         "year": year
    #     })

    # df = pd.DataFrame(items)
    # print(df)

    # return df

propHistory(input_url)


