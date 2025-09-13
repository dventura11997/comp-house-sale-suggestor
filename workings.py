import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from scrapfly import ScrapeConfig, ScrapflyClient

#url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068"


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

def compSold(soup):
    #soup = getSoup(final_url)
    prices = [p.get_text().strip() for p in soup.find_all('p', {'data-testid': 'listing-card-price'})]
    addresses = [span.get_text().strip() for span in soup.find_all('span', {'data-testid': 'address-line1'})]
    sold_info = [span.get_text().strip() for span in soup.find_all('span', class_='css-1nj9ymt')]
    
    comp_data = []
    for price, address, sold in zip(prices, addresses, sold_info):  
        sale_method = re.split(r'\d', sold)[0].strip()
        sold_date = re.search(r'\d{1,2} \w+ \d{4}', sold)
        comp_data.append({
            "price": price,
            "address": address,
            "sold_info": sold,
            "sale_method": sale_method,
            "sold_date": sold_date.group() if sold_date else None
        })

    df = pd.DataFrame(comp_data)

    # Calc Avg Price
    price_avg = pd.to_numeric(df['price'].replace('[\$,]', '', regex=True), errors='coerce').mean()
    df.drop(['sold_info'], axis=1, inplace=True)

    return df, price_avg

final_url = "https://www.domain.com.au/sold-listings/ashwood-vic-3147/house/3-bedrooms/?bathrooms=1&excludepricewithheld=1&carspaces=5-any"
soup, response_code = getSoup(final_url) 
df, price_avg = compSold(soup)

print(df)
print(price_avg)