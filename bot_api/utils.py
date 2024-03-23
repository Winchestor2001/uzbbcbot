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
    result = meters / 1000.0
    return round(result, 1) if result > 1 else 1


def filter_profile_locations(obj, lat, long):
    result = []
    for item in obj:
        print(__name__, lat, long, item.latitude, item.longitude)
        distance = calc_distance(lat, long, item.latitude, item.longitude)
        # if distance < 3:
        item.distance = distance
        result.append(item)

    return result


def count_ratings(ratings):
    voted = len(ratings)

    if voted:
        voted_stars = 0
        for rating in ratings:
            voted_stars += rating.rating * 10

        return round(voted_stars / 10 / voted, 1)
    return 0.0


def sort_subcategory(obj: list, action: str):
    result = []

    for item in obj:
        result.append(item[action])
    
    return list(set(result))


