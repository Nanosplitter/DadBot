import asyncio
import requests

APOD_URL = "https://api.nasa.gov/planetary/apod?api_key=hQqgupM0Ghb1OTjjrPkoIDw1EJq6pZQQdgMGBpnb"


async def fetch_apod(retries=3, delay_seconds=5):
    """Fetch NASA's Astronomy Picture of the Day, retrying on transient upstream errors."""
    for attempt in range(retries):
        response = requests.get(APOD_URL)
        if response.status_code == 200 and len(response.json()) > 0:
            return response.json()
        if attempt < retries - 1:
            await asyncio.sleep(delay_seconds)
    return None
