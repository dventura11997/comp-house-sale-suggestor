# Startup: 
# cd "C:\Users\danie\OneDrive\Work\Career\Coding\Folio\Comparable House Sales Suggestor\comp-house-sale-suggestor"
# env/scripts/activate
# streamlit run app.py

import streamlit as st
from pathlib import Path
import functions
from scrapfly import ScrapeConfig, ScrapflyClient

st.set_page_config(page_title="Compare Sales App", layout="wide")

# Path to the CSS file
css_file_path = Path("styles.css")

# Read the CSS file
with open(css_file_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(f"""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css?family=Libre+Bodoni|New+Amsterdam|Fredoka|Vollkorn SC" rel="stylesheet">
        <link href="styles.css" rel="stylesheet">
    </head>
            
    <div class="major-heading">
        Comparable House Sales App
    </div>
    <div class="homepage-text">
        This is a front-end for you to compare house sales with existing listings. Simply paste a domain listing in the searchbar and view relevant comparable sales instantly. Ensure the URL is the listing URL with the format like: https://www.domain.com.au/17-2-12-temple-street-ashwood-vic-3147-2020228728
    </div>
""", unsafe_allow_html=True)

# Place the text input in the first column
input_url = st.text_input("Copy in the URL:")
try:
    # Button to trigger the function once the URL is entered
    if st.button("View Comparable Sales and Property History"):
        try:
            soup, response_code = functions.getSoup(input_url)
            st.write(f"API Response code: {response_code}")
        except Exception as e:
            st.error("Error getting html from original webpage")
        try:
            price, beds, bath, parking, houseType = functions.findElements(soup)
            st.write(f"Price: {price}, Beds: {beds}, Bath: {bath}, Parks: {parking}, House Type: {houseType}")
        except Exception as e:
            st.error(f"Error extracting beds, bath, parking and house type from original webpage: {e}")
        # try:
        #     ssp = functions.extractElements(input_url)
        # except Exception as e:
        #     st.error("Error extracting suburb state and postcode from input url")
        # try:
        #     final_url = functions.constructUrl(input_url, ssp)
        # except Exception as e:
        #     st.error("Error constructing URL for comparable sales")
except Exception as e:
    st.error(str(e))
    st.stop()

#             if not final_url:
#                 st.error("Error constructing URL for comparable sales")
#             else:
#                 st.write(f"Transformed URL for comparable sales: {final_url}")

#             try:
#                 df_cs, price_avg = functions.compSold(final_url)
#             except Exception as e:
#                 st.error(f"Error with compSold function: {e}")
#                 st.stop()
#             #df_ph = functions.propHistory(input_url)

#             if df_cs is None or len(df_cs) == 0:
#                 st.info("No rows to show.")
#             else:
#                 st.metric("Average Price", f"${price_avg:,.0f}")
#                 st.dataframe(df_cs, use_container_width=True, hide_index=True)
#                 #st.link_button("Browse Sales on Domain", final_url)
#             #if df_ph is None or len(df_ph) == 0:
#                 #st.info("No rows to show.")
#             #else:
#                 #st.dataframe(df_ph, use_container_width=True, hide_index=True)
# except Exception as e:
#     st.error(str(e))
#     st.stop()

# import streamlit as st
# from scrapfly import ScrapeConfig, ScrapflyClient
# from bs4 import BeautifulSoup

# st.title("ScrapFly Test")

# url = st.text_input("URL:", "https://www.domain.com.au/11-raymond-street-ashwood-vic-3147-2020201068")
# api_key = st.text_input("ScrapFly API Key:", "scp-live-bb61fd3f185c4c6dba068babfcee3079", type="password")

# if st.button("Test Scrape"):
#     try:
#         client = ScrapflyClient(api_key)
#         result = client.scrape(ScrapeConfig(
#             url,
#             country="AU",
#             asp=True,
#             render_js=True
#         ))
        
#         soup = BeautifulSoup(result.content, 'html.parser')
#         soup_text = str(soup)
        
#         # Show first 500 chars
#         st.success("✅ Scrape successful!")
#         st.text_area("First 500 characters:", soup_text[:500])
#         st.metric("Total HTML length:", len(soup_text))
        
#         # Download button
#         st.download_button(
#             "Download HTML",
#             soup_text,
#             file_name="scraped_content.html",
#             mime="text/html"
#         )
        
#     except Exception as e:
#         st.error(f"❌ Error: {e}")

