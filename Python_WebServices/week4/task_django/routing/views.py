from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
import re
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def simple_route(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


def slug_route(request: HttpRequest):
    parameters = str(request.get_full_path()).split('/slug_route/')[1]
    result = parameters.split("/")[0]
    reg = re.compile(r"(^[0-9a-z_\.\-]{1,16}$)")
    if reg.match(result):
        return HttpResponse(result)

    return HttpResponse(status=404)


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def sum_route(request):
    parameters = str(request.get_full_path()).split('/sum_route/')[1]
    params = parameters.split("/")
    if len(params) >= 2:
        a, b = params[0], params[1]
        if check_int(a) and check_int(b):
            return HttpResponse(int(a) + int(b))
    return HttpResponse(status=404)


def sum_get_method(request: HttpRequest):
    if request.method == 'GET':
        a = request.GET.get('a', '')
        b = request.GET.get('b', '')
        if check_int(a) and check_int(b):
            return HttpResponse(int(a) + int(b))
    return HttpResponse(status=400)


@csrf_exempt
def sum_post_method(request: HttpRequest):
    if request.method == 'POST':
        a = request.POST.get('a', '')
        b = request.POST.get('b', '')
        if check_int(a) and check_int(b):
            return HttpResponse(int(a) + int(b))
    return HttpResponse(status=400)
