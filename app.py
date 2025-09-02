# Startup: 
# cd "C:\Users\danie\OneDrive\Work\Career\Coding\Folio\Comparable House Sales Suggestor\comp-house-sale-suggestor"
# env/scripts/activate
# streamlit run app.py


import streamlit as st
from pathlib import Path
import functions
import webbrowser

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
        # final_url = functions.constructUrl(input_url)
        # df_cs, price_avg = functions.compSold(final_url)
        df_ph = functions.propHistory(input_url)

        # if df_cs is None or len(df_cs) == 0:
        #     st.info("No rows to show.")
        # else:
        #     st.metric("Average Price", f"${price_avg:,.0f}")
        #     st.dataframe(df_cs, use_container_width=True, hide_index=True)
        #     st.link_button("Browse Sales on Domain", final_url)
        if df_ph is None or len(df_ph) == 0:
            st.info("No rows to show.")
        else:
            st.dataframe(df_ph, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(str(e))
    st.stop()

