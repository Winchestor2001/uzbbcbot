import logging
import math
import pandas as pd
from io import BytesIO
from .models import ServiceStuff, ProductDetail, Service, Product, City

logger = logging.getLogger('django')


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


def extract_excel_service(file, city, lang):
    excel = excel_to_bytesio(file).getvalue()
    excel_bytes_io = BytesIO(excel)
    df = pd.read_excel(excel_bytes_io)
    return sorting_to_dict(df.columns[1:], df, city, lang)


def extract_excel_product(file, city, lang):
    excel = excel_to_bytesio(file).getvalue()
    excel_bytes_io = BytesIO(excel)
    df = pd.read_excel(excel_bytes_io)
    return sorting_to_dict_product(df.columns[1:], df, city, lang)


def excel_to_bytesio(excel_file):
    df = pd.read_excel(excel_file)
    
    bytes_io = BytesIO()
    df.to_excel(bytes_io, index=False)
    bytes_io.seek(0)
    
    return bytes_io


def sorting_to_dict(columns: list, obj, city: str, lang: str):
    data = []
    for i in range(len(obj)):
        dict_data = {}
        for item in columns:
            if str(obj[item][i]) not in ["NaN", "nan"]:
                dict_data.update(
                    {
                        item: obj[item][i] if item != 'service' else Service.objects.get(uz_name=obj[item][i]),
                        "city": City.objects.get(id=city),
                        "lang": lang,
                    }
                )
        if dict_data:
            data.append(dict_data)
    return data


def sorting_to_dict_product(columns: list, obj, city: str, lang: str):
    data = []
    for i in range(len(obj)):
        dict_data = {}
        for item in columns:
            if str(obj[item][i]) not in ["NaN", "nan"]:
                dict_data.update(
                    {
                        item: obj[item][i] if item != 'product' else Product.objects.get(uz_name=obj[item][i]),
                        "city": City.objects.get(id=city),
                        "lang": lang,
                    }
                )
        if dict_data:
            data.append(dict_data)
    return data


def service_data_save_to_db(data: list):
    for item in data:
        ServiceStuff.objects.create(
            **item
        )


def product_data_save_to_db(data: list):
    for item in data:
        ProductDetail.objects.create(
            **item
        )

