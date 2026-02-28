import requests

def get_coordinates(city: str) -> tuple[float, float]:
    response = requests.get(
        'https://nominatim.openstreetmap.org/search',
        params={
            'q': city,
            'format': 'json',
            'limit': 1,
        },
        headers={'User-Agent': 'django-app'}
    )
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError('City not found')

    return float(data[0]['lat']), float(data[0]['lon'])

def get_weather(lat: float, lon: float) -> dict:
    response = requests.get(
        'https://api.open-meteo.com/v1/forecast',
        params={
            'latitude': lat,
            'longitude': lon,
            'current_weather': True,
        }
    )
    response.raise_for_status()

    return response.json()['current_weather']
