from scrapfly import ScrapeConfig, ScrapflyClient
import re
from bs4 import BeautifulSoup

ph_url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068"

scrapfly_client = ScrapflyClient("scp-live-bb61fd3f185c4c6dba068babfcee3079")
result = scrapfly_client.scrape(ScrapeConfig(
    ph_url,
    country="AU",
    asp=True,
    render_js=True
))

soup = BeautifulSoup(result.content, 'html.parser')
print(soup)

