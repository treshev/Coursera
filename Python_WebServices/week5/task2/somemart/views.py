import base64

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Review


class ItemForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=64)
    description = forms.CharField(min_length=1, max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    text = forms.CharField(min_length=1, max_length=1024)
    grade = forms.IntegerField(min_value=1, max_value=10)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):

        user = self.request.user
        print('ALTR USER: ', user)
        # Если есть заголовок `Authorization`, проверяем его.
        if "HTTP_AUTHORIZATION" in request.META:
            # В заголовке basic-авторизации две части, разделенных пробелом.
            auth = request.META["HTTP_AUTHORIZATION"].split()
            # Первая — слово "Basic"
            if len(auth) == 2 and auth[0].lower() == "basic":
                # Затем base64-кодированные имя пользователя и пароль,
                # разделенные (после декодирования) двоеточием.

                username, password = base64.b64decode(auth[1]).decode().split(":")
                # Их и используем с django.contrib.auth.authenticate
                user = authenticate(username=username, password=password)
                # from pdb import set_trace
                # set_trace()
                if user and user.is_active and user.is_staff:
                    form = ItemForm(request.POST)
                    if form.is_valid():
                        item = Item.objects.create(title=form.cleaned_data["title"],
                                                   description=form.cleaned_data["description"],
                                                   price=form.cleaned_data["price"])
                        return JsonResponse({"id": item.pk}, status=201)
                    else:
                        return HttpResponse(status=400)

        # Если не авторизовали — даем ответ с 401, требуем авторизоваться
        return HttpResponse(status=403)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            form = ReviewForm(request.POST)
            if form.is_valid():
                item = Item.objects.get(pk=item_id)
                review = Review.objects.create(text=form.cleaned_data["text"], grade=form.cleaned_data["grade"],
                                               item=item)
                return JsonResponse({"id": review.pk}, status=201)
            else:
                return HttpResponse(status=400)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.values('id', 'title', 'description', 'price').get(pk=item_id)
            rev = Review.objects.values('id', 'text', 'grade').filter(item__pk=item_id).order_by("-id")[:5]
            rev_list = list(rev)
            item["reviews"] = rev_list
            return JsonResponse(item, status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
