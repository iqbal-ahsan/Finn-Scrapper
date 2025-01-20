def flatten_dict(d):
    flat_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            flat_dict.update(flatten_dict(value)) #recursive call to flatten dic
        else:
            flat_dict[key] = value

    return flat_dict

def process_new_ads(scraped_ad_data):
    processed_ad_data = [
        {
            "_d": data.get("FINN-kode") if "FINN-kode" in data else data.get("_id"),
            **flatten_dict(data)

        }
        for data in scraped_ad_data
    ]

    return processed_ad_data