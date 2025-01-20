import requests
from bs4 import BeautifulSoup
import json
import re

# Fetch the HTML content
def search_new_ads():
    url = "https://www.finn.no/realestate/newbuildings/search.html"
    response = requests.get(url)

    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    script_tag = soup.find('script', text=re.compile(r'window\.__remixContext'))



    # Step 4: Extract the JavaScript object using regex
    if script_tag:
        script_content = script_tag.string

        # Use regex to extract the JSON-like part
        match = re.search(r'window\.__remixContext\s*=\s*({.*});', script_content,  re.DOTALL)

        if match:
            json_text = match.group(1)

            # Convert JSON text to Python dictionary
            data = json.loads(json_text)
            main_data = data['state']['loaderData']['routes/realestate+/_search+/$subvertical.search[.html]']
            search_result = main_data["results"]["docs"]

    return search_result