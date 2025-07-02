import requests
import json
import os
import datetime

# --- Constants ---
DONKI_API_BASE_URL = "https://api.nasa.gov/DONKI/"
# You can get a free API key from https://api.nasa.gov/
# For demonstration, 'DEMO_KEY' can be used, but it has rate limits.
# For production, replace with your actual API key.
NASA_API_KEY = "DEMO_KEY" 

class DONKIFetcher:
    """
    Fetches Space Weather data from NASA's DONKI API.
    """
    def __init__(self):
        print("[DONKIFetcher] Initialized.")

    def _make_api_request(self, endpoint, params=None):
        """Helper to make a request to the DONKI API."""
        if params is None:
            params = {}
        
        params['api_key'] = NASA_API_KEY
        url = f"{DONKI_API_BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"[DONKIFetcher] HTTP error occurred: {http_err} - Response: {response.text}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"[DONKIFetcher] Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"[DONKIFetcher] Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"[DONKIFetcher] An error occurred: {req_err}")
            return None
        except json.JSONDecodeError as json_err:
            print(f"[DONKIFetcher] JSON decoding error: {json_err} - Response: {response.text}")
            return None

    def get_solar_flares(self, start_date: str, end_date: str):
        """
        Fetches Solar Flare data for a given date range.
        Dates should be in YYYY-MM-DD format.
        """
        print(f"[DONKIFetcher] Fetching Solar Flares from {start_date} to {end_date}...")
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        data = self._make_api_request("FLR", params)
        if data:
            print(f"[DONKIFetcher] Found {len(data)} solar flares.")
        return data

    def get_coronal_mass_ejections(self, start_date: str, end_date: str):
        """
        Fetches Coronal Mass Ejection (CME) data for a given date range.
        Dates should be in YYYY-MM-DD format.
        """
        print(f"[DONKIFetcher] Fetching CMEs from {start_date} to {end_date}...")
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        data = self._make_api_request("CME", params)
        if data:
            print(f"[DONKIFetcher] Found {len(data)} CMEs.")
        return data
        
    def get_geomagnetic_storms(self, start_date: str, end_date: str):
        """
        Fetches Geomagnetic Storm (GST) data for a given date range.
        Dates should be in YYYY-MM-DD format.
        """
        print(f"[DONKIFetcher] Fetching Geomagnetic Storms from {start_date} to {end_date}...")
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        data = self._make_api_request("GST", params)
        if data:
            print(f"[DONKIFetcher] Found {len(data)} Geomagnetic Storms.")
        return data

# Example Usage (for testing this module independently)
if __name__ == "__main__":
    print("--- Testing DONKIFetcher Module ---")
    fetcher = DONKIFetcher()
    
    today = datetime.date.today()
    past_week = today - datetime.timedelta(days=7)
    
    start_date_str = past_week.strftime("%Y-%m-%d")
    end_date_str = today.strftime("%Y-%m-%d")

    print(f"\n--- Solar Flares ({start_date_str} to {end_date_str}) ---")
    flares = fetcher.get_solar_flares(start_date_str, end_date_str)
    if flares:
        for flare in flares:
            print(f"  Flare Class: {flare.get('classType', 'N/A')}, Peak Time: {flare.get('peakTime', 'N/A')}")
    else:
        print("  No solar flares found or error fetching data.")

    print(f"\n--- Coronal Mass Ejections ({start_date_str} to {end_date_str}) ---")
    cmes = fetcher.get_coronal_mass_ejections(start_date_str, end_date_str)
    if cmes:
        for cme in cmes:
            print(f"  CME Time: {cme.get('startTime', 'N/A')}, Speed: {cme.get('speed', 'N/A')} km/s")
    else:
        print("  No CMEs found or error fetching data.")
        
    print(f"\n--- Geomagnetic Storms ({start_date_str} to {end_date_str}) ---")
    gsts = fetcher.get_geomagnetic_storms(start_date_str, end_date_str)
    if gsts:
        for gst in gsts:
            print(f"  GST Start Time: {gst.get('startTime', 'N/A')}, Kp Index: {gst.get('kpIndex', 'N/A')}")
    else:
        print("  No Geomagnetic Storms found or error fetching data.")

    print("--- DONKIFetcher Test Finished ---")