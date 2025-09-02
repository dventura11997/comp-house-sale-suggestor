import re

input_url = "https://www.domain.com.au/17-2-12-temple-street-ashwood-vic-3147-2020228728"

output_url = re.sub(r'-(\d+)$', '', input_url)           # remove the trailing -digits
output_url = output_url.replace(".com.au/", ".com.au/property-profile/")

print(output_url)

