from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed


def simple_route(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed('GET')


def slug_route(request: HttpRequest, slug):
    return HttpResponse(slug)


def sum_route(request, a, b):
    try:
        return HttpResponse(int(a) + int(b))
    except ValueError:
        return HttpResponse(status=400)


def sum_get_method(request: HttpRequest):
    if request.method == 'GET':
        a = request.GET.get('a', '')
        b = request.GET.get('b', '')
        try:
            return HttpResponse(int(a) + int(b))
        except ValueError:
            return HttpResponse(status=400)
    return HttpResponseNotAllowed('GET')


def sum_post_method(request: HttpRequest):
    if request.method == 'POST':
        a = request.POST.get('a', '')
        b = request.POST.get('b', '')
        try:
            return HttpResponse(int(a) + int(b))
        except ValueError:
            return HttpResponse(status=400)
    return HttpResponseNotAllowed('POST')
