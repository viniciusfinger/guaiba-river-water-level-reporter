from river_registry import RiverRegistry
from pdf_service import create_pdf_report

def process_river_level(river_level_list: list[RiverRegistry]):
    variation_1h = round(river_level_list[-1].river_level - river_level_list[-5].river_level, 2)
    print(f"Variation 1h: {variation_1h} meters. - From {river_level_list[-1].date} to {river_level_list[-5].date}")

    variation_6h = round(river_level_list[-1].river_level - river_level_list[-25].river_level, 2)
    print(f"Variation 6h: {variation_6h} meters. - From {river_level_list[-1].date} to {river_level_list[-25].date}")
    
    variation_24h = round(river_level_list[-1].river_level - river_level_list[0].river_level, 2)
    print(f"Variation 24h: {variation_24h} meters. - From {river_level_list[-1].date} to {river_level_list[0].date}")
    

    flood_alert = is_flood_alert(river_level_list[-1])
    if flood_alert:
        send_flood_alert()
    
    create_pdf_report(river_level_list, variation_1h, variation_6h, variation_24h, flood_alert)
    
def is_flood_alert(last_registry: RiverRegistry) -> bool:
    return last_registry.river_level > 3.6

def send_flood_alert():
    print("🚨 Flood alert")
