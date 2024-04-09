from modeltranslation.translator import register, TranslationOptions
from .models import City, Region


@register(City)
class CityTranslation(TranslationOptions):
    fields = ["name"]


@register(Region)
class RegionTranslation(TranslationOptions):
    fields = ["name"]


