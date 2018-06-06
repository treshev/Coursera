from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def echo(request: HttpRequest):
    statement = request.META.get("HTTP_HOST", "empty")
    return render(request, 'echo.html', context={'statement': statement})


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
