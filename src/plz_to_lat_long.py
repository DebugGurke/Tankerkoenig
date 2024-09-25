import requests
from typing import Tuple, Optional

def get_lat_long_from_postal(postal_code:str, country:str="de") -> Optional[Tuple[float, float]]:
    """
    Convert a postal code into latitude and longitude using the Nominatim API.

    :param postal_code: Postal code to be converted.
    :param country: Country code (default: 'de' for Germany).
    :return: Tuple with latitude and longitude, or None if not found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "postalcode": postal_code,
        "country": country,
        "format": "json",
        "limit": 1
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        else:
            print(f"No data found for postal code: {postal_code}")
            return None
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")
        return None


def main() -> None:
    
    postal_code = input("Enter the postal code: ")
    country_code = input("Enter the country code (default is 'de' for Germany): ") or "de"

    result = get_lat_long_from_postal(postal_code, country_code)
    
    if result:
        lat, lon = result
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("Could not find the location for the given postal code.")


if __name__ == "__main__":
    main()
