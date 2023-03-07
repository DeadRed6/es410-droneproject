from haversine_function import get_distance_haversine  # import the get_distance function from previous example

def test_same_location():
    lat1, lon1, lat2, lon2 = 40.754, -73.984, 40.754, -73.984
    dx, dy = get_distance_haversine(lat1, lon1, lat2, lon2)
    assert dx == 0 and dy == 0

def test_same_latitude():
    lat1, lon1, lat2, lon2 = 40.754, -73.984, 40.754, -73.983
    dx, dy = get_distance_haversine(lat1, lon1, lat2, lon2)
    assert round(dx, 3) == 11.022 and dy == 0

def test_same_longitude():
    lat1, lon1, lat2, lon2 = 40.754, -73.984, 40.753, -73.984
    dx, dy = get_distance_haversine(lat1, lon1, lat2, lon2)
    assert dx == 0 and round(dy, 3) == 123.079

def test_different_locations():
    lat1, lon1, lat2, lon2 = 40.754, -73.984, 40.755, -73.983
    dx, dy = get_distance_haversine(lat1, lon1, lat2, lon2)
    assert round(dx, 3) == 11.148 and round(dy, 3) == 78.495
