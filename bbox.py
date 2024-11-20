import math
from config.config import Config
from constants import frame

def calculate_bounding_box(center_lat, center_lon, height_km, aspect_ratio=1.0):
    """
    Calculate geographic coordinates of a bounding box given a center point,
    width, and aspect ratio.
    
    Args:
        center_lat (float): Center latitude in degrees
        center_lon (float): Center longitude in degrees
        height_km (float): Height of the box in kilometers
        aspect_ratio (float): Desired height/width ratio (default: 1.0 for square)
    
    Returns:
        tuple: (min_lat, max_lat, min_lon, max_lon)
    """
    # Earth's radius in kilometers
    EARTH_RADIUS = 6371.0
    
    # Calculate width based on aspect ratio
    width_km = height_km / aspect_ratio
    
    # Convert distances to degrees
    # For longitude, adjust for latitude's effect on distance
    lat_degree = (height_km / 2) / (EARTH_RADIUS * math.pi / 180)
    lon_degree = (width_km / 2) / (EARTH_RADIUS * math.pi / 180)
    lon_degree = lon_degree / math.cos(math.radians(center_lat))
    
    # Calculate bounds
    min_lat = center_lat - lat_degree
    max_lat = center_lat + lat_degree
    min_lon = center_lon - lon_degree
    max_lon = center_lon + lon_degree
    
    return (min_lat, max_lat, min_lon, max_lon)

# Example usage
if __name__ == "__main__":
    config = Config.instance()
    
    latitude = config['forecast']['lat']
    longitude = config['forecast']['lon']
    box = calculate_bounding_box(float(latitude), float(longitude), height_km=90, aspect_ratio=frame.HEIGHT_LESS_INFO/frame.WIDTH)
    print(f"Bounding box coordinates: {box}")