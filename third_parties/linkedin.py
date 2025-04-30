import os
from dotenv import load_dotenv
import requests

load_dotenv()


def scrape_linkedin_profile(profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles.
    Manually scrape information from LinkedIn profile."""

    if mock:
        response = requests.get(profile_url, timeout=10)
    else:
        scrapein_api_key = os.environ.get("SCRAPEIN_API_KEY")
        scrapein_endpoint = f"https://api.scrapin.io/enrichment/profile"
        query_params = {"linkedInUrl": profile_url, "apiKey": scrapein_api_key}

        response = requests.get(scrapein_endpoint, params=query_params, timeout=10)
    
    data = response.json().get("person")

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
    }

    return data



if __name__ == "__main__":
    URL = "https://gist.githubusercontent.com/TareqMonwer/f2bd6927aff7caa6efea1f67481c8641/raw/15d48642c7beab488bef35c61c044c3fde4c741e/profile_1.json"
    scrape_linkedin_profile(URL, True)