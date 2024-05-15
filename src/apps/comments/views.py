from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from bot_api.models import ServiceRating, ProductRating, AboutBot
from django.http.response import HttpResponseBadRequest


class CommentsTemplateView(TemplateView):
    template_name = "comments.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        _type = self.request.GET.get('type')
        title = self.request.GET.get('title', 'Comments')
        _id = self.request.GET.get('id')
        configs = AboutBot.objects.all()
        if _type == 'service':
            comments = ServiceRating.objects.filter(stuff__id=_id).order_by('-created_at')
        elif _type == 'product':
            comments = ProductRating.objects.filter(product_detail__id=_id).order_by('-created_at')
        else:
            raise HttpResponseBadRequest()
        kwargs['comments'] = comments
        kwargs['configs'] = configs
        kwargs['title'] = title
        return super().get_context_data(**kwargs)
