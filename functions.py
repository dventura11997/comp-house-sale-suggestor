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

#url = "https://www.domain.com.au/13-700-riversdale-road-camberwell-vic-3124-2020196506"

# URL to scrape
def get_url(input_url):
    return input_url

def extractElements(input_url):
    try:
        match = re.search(r'([a-z]+)-(vic|nsw|qld|wa|sa|tas|nt|act)-(\d{4})', input_url)
        ssp = match.group(0)
        
        return ssp
    except Exception as e:
        print("Error extracting elements from url:", e)


def getSoup(input_url):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
        response = requests.get(input_url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def findElements(input_url):
    soup = getSoup(input_url)
    
    try:
        # price
        price_element = soup.find('div', {'data-testid': 'listing-details__summary-title'}).find('span')
        price = price_element.text
        #print("price:", price)
    except Exception as e:
        print("Error finding price:", e)
    
    try:
        # beds
        beds_container = soup.find('span', string='Beds').parent
        beds = beds_container.get_text().strip().split()[0]
        #print("beds:", beds)
    except Exception as e:
        print("Error finding beds:", e)

    try:
        # bath
        bath_container = soup.find('span', string='Bath').parent
        bath = bath_container.get_text().strip().split()[0]
        #print("bath:", bath)
    except Exception as e:
        print("Error finding price element:", e)
    
    try:
        # bath
        parking_container = soup.find('span', string='Parking').parent
        parking = parking_container.get_text().strip().split()[0]
        #print("parking:", parking)
    except Exception as e:
        print("Error finding parking:", e)
    
    try:
        # House Type
        houseType_element = soup.find('div', {'data-testid': 'listing-summary-property-type'}).find('span')
        houseType = houseType_element.get_text().strip().split()[0]
        if houseType == "Townhouse": houseType = "town-house"
        print("House Type:", houseType)
    except Exception as e:
        print("Error finding house type:", e)


    return price, beds, bath, parking, houseType

def constructUrl(input_url):
    base_url = "https://www.domain.com.au/sold-listings/"
    ssp = extractElements(input_url)
    #print(ssp)
    price, beds, bath, parking, houseType = findElements(input_url)
    #print(price, beds, bath, parking, houseType)
    final_url = base_url + ssp + "/" + houseType + "/" + beds + "-bedrooms/?bathrooms=" + bath + "&excludepricewithheld=1&carspaces=" + parking
    print(final_url)

    return final_url


def compSold(final_url):
    soup = getSoup(final_url)
    prices = [p.get_text().strip() for p in soup.find_all('p', {'data-testid': 'listing-card-price'})]
    addresses = [span.get_text().strip() for span in soup.find_all('span', {'data-testid': 'address-line1'})]
    sold_info = [span.get_text().strip() for span in soup.find_all('span', class_='css-1nj9ymt')]

    # Create dataframe (assuming equal lengths)
    df = pd.DataFrame({
    'price': prices,
    'address': addresses, 
    'sold_info': sold_info
    })

    df['sale_methods'] = [re.split(r'\d', text)[0].strip() for text in df['sold_info']]
    df['sold_dates'] = [re.search(r'\d{1,2} \w+ \d{4}', text).group() if re.search(r'\d{1,2} \w+ \d{4}', text) else None for text in df['sold_info']]

    # Calc Avg Price
    price_avg = pd.to_numeric(df['price'].replace('[\$,]', '', regex=True), errors='coerce').mean()
    df.drop(['sold_info'], axis=1, inplace=True)

    return df, price_avg



def propHistory(input_url):
    ph_url = re.sub(r'-(\d+)$', '', input_url)           # remove the trailing -digits
    ph_url = ph_url.replace(".com.au/", ".com.au/property-profile/")
    print(ph_url)

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.get(ph_url)
    time.sleep(1)
    button = browser.find_element(By.XPATH, "//button[text()='View more results']")
    button.click()
    soup = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(4)
    browser.quit()

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

    return df






