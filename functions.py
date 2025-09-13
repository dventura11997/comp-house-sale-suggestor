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


    return price, beds, bath, parking, houseType

def constructUrl(ssp, beds, bath, parking, houseType):
    base_url = "https://www.domain.com.au/sold-listings/"
    #ssp = extractElements(input_url)
    #price, beds, bath, parking, houseType = findElements(input_url)
    final_url = base_url + ssp + "/" + houseType + "/" + beds + "-bedrooms/?bathrooms=" + bath + "&excludepricewithheld=1&carspaces=" + parking
    print(final_url)

    return final_url


# def compSold(final_url):
#     soup = getSoup(final_url)
#     prices = [p.get_text().strip() for p in soup.find_all('p', {'data-testid': 'listing-card-price'})]
#     addresses = [span.get_text().strip() for span in soup.find_all('span', {'data-testid': 'address-line1'})]
#     sold_info = [span.get_text().strip() for span in soup.find_all('span', class_='css-1nj9ymt')]

#     # Create dataframe (assuming equal lengths)
#     df = pd.DataFrame({
#     'price': prices,
#     'address': addresses, 
#     'sold_info': sold_info
#     })

#     df['sale_methods'] = [re.split(r'\d', text)[0].strip() for text in df['sold_info']]
#     df['sold_dates'] = [re.search(r'\d{1,2} \w+ \d{4}', text).group() if re.search(r'\d{1,2} \w+ \d{4}', text) else None for text in df['sold_info']]

#     # Calc Avg Price
#     price_avg = pd.to_numeric(df['price'].replace('[\$,]', '', regex=True), errors='coerce').mean()
#     df.drop(['sold_info'], axis=1, inplace=True)

#     return df, price_avg


# def propHistory(input_url):
#     ph_url = re.sub(r'-(\d+)$', '', input_url)           
#     ph_url = ph_url.replace(".com.au/", ".com.au/property-profile/")

#     soup = getSoup(ph_url)
    
#     items = []
#     list_element = soup.find('ul', {'class': 'css-m3i618'})

#     if list_element:
#         for li in list_element.find_all("li", {"class": "css-16ezjtx"}):
#             try:
#                 category = li.find('div', {'data-testid': 'fe-co-property-timeline-card-category'}).get_text(strip=True)
#                 price = li.find('span', {'data-testid': 'fe-co-property-timeline-card-heading'}).get_text(strip=True)
#                 period = li.find('span', {'data-testid': 'fe-co-property-timeline-card-heading'}).find_next('span').get_text(strip=True)
#                 month = li.find('div', {'class': 'css-vajoca'}).get_text(strip=True).upper()
#                 year = li.find('div', {'class': 'css-1qi20sy'}).get_text(strip=True)

#                 items.append({
#                     "category": category,
#                     "price": price,
#                     "period": period,
#                     "month": month,
#                     "year": year
#                 })
#             except Exception as e:
#                 print(f"Error parsing item: {e}")
#         df = pd.DataFrame(items)
#     else:
#         return pd.DataFrame()

#     return df
    







