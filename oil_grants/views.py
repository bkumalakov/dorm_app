from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *


class MainView(View):
    def get(self, request):
        competitions = Competitions.objects.all()
        check_dates(competitions)
        return render(request, "oil_grants/home.html", context={'competitions': competitions, })
