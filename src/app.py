
import requests
import json
from typing import List, Dict
from plz_to_lat_long import get_lat_long_from_postal
from env import load

env_vars = load("tk.env")

API_BASE_URL = "https://creativecommons.tankerkoenig.de/json/list.php"
API_KEY = env_vars.get("API_KEY", "NOPE")  # API KEY
POSTAL_CODE = "10115" # plz as string 10115 in Berlin
COUNTRY = "de" # country code
RADIUS = 5  # km

def get_gas_prices(lat:float, lng:float, rad:int, sort:str="dist") -> Dict:
    """
    Fetches gas prices from tankerkoenig.de based on location.
    
    :param lat: (float) Latitude of the location.
    :param lng: (float) Longitude of the location.
    :param rad: (int) Search radius in km.
    :param sort: (str) Sort results by 'dist' (distance) or 'price'.
    :return: (dict) Dictionary with response data.
    """
    params = {
        "lat": lat,
        "lng": lng,
        "rad": rad,
        "sort": sort,
        "type": "all",
        "apikey": API_KEY
    }

    response = requests.get(API_BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def display_gas_prices(gas_stations:List[Dict], limit:int=-1) -> None:
    """
    Print a list of gas stations on the terminal
    
    :param gas_stations: (list) List of gas stations
    :param limit: (int) limits the output to n values, default: all
    :return: None
    """
    
    # if not limit:
    #     limit = len(gas_stations)
    
    print(f"{'Name':30} {'Brand':10} {'Diesel':8} {'E5':8} {'E10':8} {'Distance (km)':12}")
    print("-" * 80)

    for station in gas_stations[:limit]:
        name = station.get("name", "Unknown")
        brand = station.get("brand", "Unknown")
        diesel = station.get("diesel", "N/A")
        e5 = station.get("e5", "N/A")
        e10 = station.get("e10", "N/A")
        distance = station.get("dist", "N/A")

        print(f"{name[:30]:30} {brand[:10]:10} {diesel:8} {e5:8} {e10:8} {distance:12}")


def main() -> None:
        
    try:
        latitude, longitude = get_lat_long_from_postal(POSTAL_CODE, COUNTRY)
    
    except:
        print("error loading lat long")
        exit()

    try:
        gas_data = get_gas_prices(lat=latitude, lng=longitude, rad=RADIUS)
        
        if gas_data.get("ok", False):
            stations = gas_data.get("stations", [])
            display_gas_prices(stations, limit=5)
        else:
            print("Error: Unable to fetch gas prices.")
            
    except requests.RequestException as e:
        print(f"An error occurred while fetching gas prices: {e}")


if __name__ == "__main__":
    main()
