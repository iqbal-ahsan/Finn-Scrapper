import json
import requests
from bs4 import BeautifulSoup

def scrape_new_ads(ad_data):
    
    ad_urls = []
    for data in ad_data:
        ad_urls.append(data["canonical_url"])

    scraped_ad_data = []
    for url in ad_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_section = soup.find("section", {"aria-label":"Tittel"})
        heading = title_section.find("h1").text.strip()
        subheading = title_section.find("h2").text.strip() if title_section.find("h2") else None

        key_info_section = soup.find("section", {"aria-labelledby":"keyinfo-heading"})
        key_info_dict = {}
        if key_info_section:
            for dt_elements in key_info_section.find_all("dt"):
                dd_element = dt_elements.find_next_sibling("dd")
                key_info_dict[dt_elements.text.strip()] = dd_element.text.strip()

        cadastre_section = key_info_section.find("section", {"aria-labelledby":"cadastreinfo-part"})
        cadastre_info_dict = {}
        if cadastre_section:
            for div in cadastre_section.find_all("div"):
                key, value = div.text.strip().split(":", 1)
                cadastre_info_dict[key.strip()] = value.strip()

        finn_info_section = soup.find("section", {"aria-labelledby":"ad-info-heading"})
        table = finn_info_section.find('table')
        finn_info_dict = {}
        flag=1
        if table:
            for row in table.find_all('tr'):
                if flag < 3:
                    key = row.find('th').text.strip()
                    value = row.find('td').text.strip()
                    finn_info_dict[key] = value
                    flag += 1

        scraped_ad_data.append({
            'heading': heading,
            'subheading': subheading,
            'key_info_1': key_info_dict,
            'key_info_2': cadastre_info_dict,
            'finn_info':finn_info_dict
        })

    return scraped_ad_data