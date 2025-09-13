import re

input_url = "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068"

def extractElements(input_url):
    try:
        match = re.search(r'([a-z]+)-(vic|nsw|qld|wa|sa|tas|nt|act)-(\d{4})', input_url)
        ssp = match.group(0)
        
        return ssp if ssp else None
    except Exception as e:
        print("Error extracting elements from url:", e)



def constructUrl(input_url):
    base_url = "https://www.domain.com.au/sold-listings/"
    ssp = extractElements(input_url)
    #price, beds, bath, parking, houseType = findElements(input_url)
    #final_url = base_url + ssp + "/" + houseType + "/" + beds + "-bedrooms/?bathrooms=" + bath + "&excludepricewithheld=1&carspaces=" + parking
    print(ssp)


constructUrl(input_url)