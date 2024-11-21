class RiverRegistry:
    def __init__(self, date, river_level):
        self.date = date
        self.river_level = river_level
        
    def __str__(self):
        return f"Date: {self.date}, River Level: {self.river_level}"
