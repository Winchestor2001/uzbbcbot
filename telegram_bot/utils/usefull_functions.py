import requests
import json


def location_info(lat, lon):
    lat, lon = float(lat), float(lon)
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json")
    if response.status_code == 200:
        response_text = response.content.decode('utf-8')

        # Convert the decoded content to JSON
        data = json.loads(response_text)['address']
        # data = response.json()['address']
        country = data.get('country', 'unknown')
        city = data.get('city', 'unknown')
        suburb = data.get('suburb', 'unknown')

        return f"{country}, {city}, {suburb}"


async def get_region_cities(obj: list, region: str):
    for item in obj:
        if item['name'] == region:
            return item['cities']

