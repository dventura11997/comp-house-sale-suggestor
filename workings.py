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

def propHistory(input_url):
    ph_url = re.sub(r'-(\d+)$', '', input_url)           
    ph_url = ph_url.replace(".com.au/", ".com.au/property-profile/")
    print(ph_url)

    soup, response_code = getSoup(ph_url)
    
    items = []
    list_element = soup.find('ul', {'class': 'css-m3i618'})

    if list_element:
        for li in list_element.find_all("li", {"class": "css-16ezjtx"}):
            try:
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
            except Exception as e:
                print(f"Error parsing item: {e}")
        df = pd.DataFrame(items)
    else:
        return pd.DataFrame()

    return df

input_url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068" 
df = propHistory(input_url)

print(df)
