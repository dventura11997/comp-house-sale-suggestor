import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from scrapfly import ScrapeConfig, ScrapflyClient

#url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068"

# URL to scrape
def get_url(input_url):
    return input_url

def extractElements(input_url):
    try:
        match = re.search(r'([a-z]+)-(vic|nsw|qld|wa|sa|tas|nt|act)-(\d{4})', input_url)
        ssp = match.group(0)
        
        return ssp if ssp else None
    except Exception as e:
        print("Error extracting elements from url:", e)


def getSoup(input_url):
    try:
        scrapfly_client = ScrapflyClient("scp-live-bb61fd3f185c4c6dba068babfcee3079")
        response = scrapfly_client.scrape(ScrapeConfig(
            input_url,
            country="AU",
            asp=True,
            render_js=True
        ))
        print(f"Status code: {response.status_code}")
        soup = BeautifulSoup(response.content, 'html.parser')
        response_code = response.status_code
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code} from target (likely bot protection).")
        # if "KPSDK" in response.content or "Access Denied" in response.content:
        #     raise RuntimeError("Blocked by bot protection.")
        return soup, response_code
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def findElements(soup):
    #soup = getSoup(input_url)
    price = beds = bath = parking = houseType = None

    try:
        # price
        price_element = soup.find('div', {'data-testid': 'listing-details__summary-title'}).find('span')
        price = price_element.text
    except Exception as e:
        print("Error finding price:", e)
    
    try:
        # beds
        beds_container = soup.find('span', string='Beds').parent
        beds = beds_container.get_text().strip().split()[0]
    except Exception as e:
        print("Error finding beds:", e)

    try:
        # bath
        bath_container = soup.find('span', string='Bath').parent
        bath = bath_container.get_text().strip().split()[0]
    except Exception as e:
        print("Error finding price element:", e)
    
    try:
        # bath
        parking_container = soup.find('span', string='Parking').parent
        parking = parking_container.get_text().strip().split()[0]
    except Exception as e:
        print("Error finding parking:", e)
    
    try:
        # House Type
        houseType_element = soup.find('div', {'data-testid': 'listing-summary-property-type'}).find('span')
        houseType = houseType_element.get_text().strip().split()[0]
        if houseType == "Townhouse": houseType = "town-house"
    except Exception as e:
        print("Error finding house type:", e)

    print(price, beds, bath, parking, houseType)

    return price, beds, bath, parking, houseType

input_url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068"
soup, response_code = getSoup(input_url)
findElements(soup)