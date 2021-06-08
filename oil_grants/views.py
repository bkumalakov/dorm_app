from django.http import HttpResponse


def studentRating(request):
    return HttpResponse("Страница рейтинга обучающихся.")


def oilCompanyMoney(request):
    return HttpResponse("Таблица с суммами недропользователей.")
