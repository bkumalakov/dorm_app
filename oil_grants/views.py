from django.http import HttpResponse
from django.shortcuts import render


def studentRating(request):
    return render(
        request,
        'oil_grant/index.html',
        context={'page_title': 'Рейтинг обучающихся'},)
