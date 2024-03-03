import math


def calc_distance(lat1, lon1, lat2, lon2):
    r = 6371000
    lat1, lat2, lon1, lon2 = float(lat1), float(lat2), float(lon1), float(lon2)
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = r * c  # output distance in meters
    return meters / 1000.0  # output distance in kilometers


def filter_profile_locations(obj, lat, long):
    result = []
    for item in obj:
        print(__name__, lat, long, item.latitude, item.longitude)
        distance = calc_distance(lat, long, item.latitude, item.longitude)
        # if distance < 3:
        item.distance = distance
        result.append(item)

    return result

