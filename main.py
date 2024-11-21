import time
from river_registry import RiverRegistry
from river_level_service import get_river_level
from river_registry_processor import process_river_level

REPORT_INTERVAL = 60 # in seconds

while True:
    river_level_list: list[RiverRegistry] = get_river_level()
    process_river_level(river_level_list)
    time.sleep(REPORT_INTERVAL)
