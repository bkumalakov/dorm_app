
from django.http import HttpResponse


def dummy(request):
    return HttpResponse("Hello, world. You're at the polls index.")
