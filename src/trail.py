
import requests
from utilities.states import LocationOutput

def get_location()->LocationOutput:
    response = requests.get('https://ipinfo.io/json')
    result = response.json()
    country= str(result["country"])
    location_reuslt=LocationOutput(country=country.lower())
    return location_reuslt

loc = get_location()
print(loc)

