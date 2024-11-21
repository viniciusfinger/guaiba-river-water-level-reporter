import requests
from datetime import datetime
from river_registry import RiverRegistry

def get_river_level():
    try:
        response = requests.get('https://nivelguaiba.com.br/portoalegre.json')
        data = response.json()

        river_registry = []
        
        for date_str, level in data.items():
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
            river_registry.append(RiverRegistry(date, level))
    except Exception as e:
        print(f"Error fetching data: {e}")

    return river_registry
