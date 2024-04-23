import logging
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_api.serializers import AboutBotSerializer, CitySerializer, TelegramUserSerializer, RegionsSerializer, ServiceSerializer, ServiceCategorySerializer, \
    ServiceStuffSerializer, StuffCommentsSerializer, ProductCategorySerializer, ProductDetailSerializer, \
    ProductCommentsSerializer
from . import models
from .utils import excel_to_bytesio, extract_excel, sort_subcategory
from django.core.paginator import Paginator
from celery_tasks.models import NotifyTasks


logger = logging.getLogger('django')


class TelegramUserCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        tg_user = models.TgUser.objects.get(user_id=user_id)
        serializer = TelegramUserSerializer(instance=tg_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        tg_user = models.TgUser.objects.filter(user_id=user_id)
        if tg_user.exists():
            serializer = TelegramUserSerializer(instance=tg_user.first())
            stat = status.HTTP_200_OK
        else:
            serializer = TelegramUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            stat = status.HTTP_201_CREATED
        return Response(serializer.data, status=stat)


class TelegramUserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TelegramUserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = models.TgUser
    lookup_field = 'user_id'


class RegionsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        regions = models.Region.objects.filter(is_visible=True)
        lang = request.GET.get('lang')
        serializer_context = {'lang': lang}
        serializer = RegionsSerializer(instance=regions, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserInfoAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        user_id = request.data['user_id']
        phone_number = request.data.get('phone_number', False)
        city = request.data.get('city', "no")
        user = models.TgUser.objects.get(user_id=int(user_id))
        user.phone_number = phone_number if phone_number else user.phone_number
        user.city.clear()
        if city != 'no':
            city_obj = models.City.objects.filter(name=city)
            if city_obj.exists():
                user.city.add(city_obj.first().pk)
            else:
                region = models.Region.objects.get(name=city)
                cities = models.City.objects.filter(region=region)
                for c in cities:
                    user.city.add(c)
                user.single_regions = True

            user.all_regions = False
        else:
            user.all_regions = True
        user.is_active = True
        user.save()
        serializer = TelegramUserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class SearchServiceAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        limit = 5
        user_id = request.GET['user_id']
        service = request.GET['service']
        lang = request.GET['lang']
        offset = int(request.GET['offset'])
        user = models.TgUser.objects.get(user_id=int(user_id))
        if user.all_regions:
            services = models.ServiceStuff.objects.filter(lang=lang).order_by('-rating')
        else:
            services = models.ServiceStuff.objects.filter(lang=lang, city__in=user.city.all(), service__name=service).order_by('-rating')

        total_services = len(services)
        p = Paginator(services, limit)
        services = p.page(offset)
        serializer_context = {"lang": lang}
        serializer = ServiceStuffSerializer(instance=services, many=True, context=serializer_context)
        user_serizlier = TelegramUserSerializer(instance=user)
        return Response({'services': serializer.data, 'user': user_serizlier.data, 'total_services': total_services},
                        status=status.HTTP_200_OK)


class CallAPIView(TemplateView):
    template_name = 'call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone'] = self.request.GET.get('phone')
        user = models.TgUser.objects.get(user_id=self.request.GET.get('user_id'))
        NotifyTasks.objects.create(
            user=user,
            receiver=self.request.GET.get('id'),
            type=self.request.GET.get('type')
        )
        return context


class GetAllServiceAPIView(APIView):
    def get(self, request, *args, **kwargs):
        services = models.ServiceCategory.objects.all()
        lang = request.GET.get('lang')
        serializer_context = {'lang': lang}
        serializer = ServiceCategorySerializer(instance=services, many=True, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StuffServiceAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        stuff_id = request.GET['stuff_id']
        lang = request.GET['lang']
        lang = request.GET.get('lang')
        serializer_context = {'lang': lang}
        stuff_service = models.ServiceStuff.objects.get(id=stuff_id)
        serializer = ServiceStuffSerializer(instance=stuff_service, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StuffCommentsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        stuff_id = request.GET['id']
        stuff_comments = models.ServiceRating.objects.filter(stuff__id=stuff_id).order_by('-created_at')
        serializer = StuffCommentsSerializer(instance=stuff_comments[:3], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        service_id = request.data.get('service_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        models.ServiceRating.objects.create(
            tg_user=models.TgUser.objects.get(user_id=user_id),
            stuff=models.ServiceStuff.objects.get(id=service_id),
            rating=rating,
            comment=comment
        )


class GetAllProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = models.ProductCategory.objects.all()
        serializer = ProductCategorySerializer(instance=products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchProductAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        limit = 3
        user_id = request.GET['user_id']
        product = request.GET['product']
        lang = request.GET['lang']
        offset = int(request.GET['offset']) - 1
        user = models.TgUser.objects.get(user_id=int(user_id))
        if user.all_regions:
            products = models.ProductDetail.objects.filter(lang=lang).order_by('-rating')
        else:
            products = models.ProductDetail.objects.filter(lang=lang, city__in=user.city.all(), product__name=product).order_by('-rating')
        total_products = len(products)
        serializer_context = {"lang": lang}
        serializer = ProductDetailSerializer(instance=products[offset:offset + limit], many=True, context=serializer_context)
        user_serizlier = TelegramUserSerializer(instance=user)
        return Response({'products': serializer.data, 'user': user_serizlier.data, 'total_products': total_products},
                        status=status.HTTP_200_OK)


class ProductInfoAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product_id = request.GET['product_id']
        lang = request.GET['lang']
        product = models.ProductDetail.objects.get(id=product_id)
        serializer_context = {"lang": lang}
        serializer = ProductDetailSerializer(instance=product, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCommentsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product_id = request.GET['product_id']
        product_comments = models.ProductRating.objects.filter(product_detail__id=product_id).order_by('-created_at')
        serializer = ProductCommentsSerializer(instance=product_comments[:3], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        models.ProductRating.objects.create(
            tg_user=models.TgUser.objects.get(user_id=user_id),
            product_detail=models.ProductDetail.objects.get(id=product_id),
            rating=rating,
            comment=comment
        )


class SearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        user = models.TgUser.objects.get(user_id=request.GET['user_id'])
        services = models.ServiceStuff.objects.filter(service__name__icontains=q).filter(city__in=user.city.all())
        if services.exists():
            serializer = ServiceStuffSerializer(instance=services, many=True)
            serializer = sort_subcategory(serializer.data, 'service')
            return Response({"result": serializer, "to_state": "service"}, status=status.HTTP_200_OK)
        else:
            products = models.ProductDetail.objects.filter(product__name__icontains=q).filter(city__in=user.city.all())
            serializer = ProductDetailSerializer(instance=products, many=True)
            serializer = sort_subcategory(serializer.data, 'product')
            return Response({"result": serializer, "to_state": "product"}, status=status.HTTP_200_OK)


class AboutBotAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        about_bot = models.AboutBot.objects.first()
        serializer = AboutBotSerializer(instance=about_bot)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetCities(generics.ListAPIView):
    queryset = models.City
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        region_id = request.GET.get("region_id")
        query = models.City.objects.filter(region__id=region_id)
        serializer = self.get_serializer(instance=query, many=True)
        return Response({"cities": serializer.data}, status=200)


def get_service_excel(request):
    if request.method == 'POST':
        lang = request.POST.get('lang')
        file = request.FILES.get("excel")
        region = request.POST.get("region")
        city = request.POST.get("city")
        data = extract_excel(file)
        
    return redirect('/admin/')


def get_product_excel(request):
    if request.method == 'POST':
        lang = request.POST.get('lang')
        file = request.FILES["excel"]
        region = request.POST.get("region")
        city = request.POST.get("city")
        data = extract_excel(file)
    return redirect('/admin/')


def dashboard_callback(request, context):
    regions = models.Region.objects.filter(is_visible=True)
    cities = models.City.objects.all()
    context.update({
        "regions": regions,
        "cities": cities,
    })

    return context
