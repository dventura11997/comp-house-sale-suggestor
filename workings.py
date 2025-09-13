import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from scrapfly import ScrapeConfig, ScrapflyClient

#url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068"


def extractElements(input_url):
    try:
        match = re.search(r'(?:street|road|avenue|grove|drive|lane|court|place|way|close|crescent)-([a-z]+(?:-[a-z]+)*)-(vic|nsw|qld|wa|sa|tas|nt|act)-(\d{4})', input_url)
        ssp = match.group(1) + '-' + match.group(2) + '-' + match.group(3) if match else None
        
        return ssp if ssp else None
    except Exception as e:
        print("Error extracting elements from url:", e)


#input_url = "https://www.domain.com.au/170-burke-road-glen-iris-vic-3146-2020215095" 
input_url = "https://www.domain.com.au/3-29-ashburn-grove-ashburton-vic-3147-2020227477" 
ssp = extractElements(input_url)

print(ssp)
