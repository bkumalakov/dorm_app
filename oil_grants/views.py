from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View
from django.db.models import Q
from .models import *


def get_or_pass(student, competition):
    try:
        application = Applications.objects.get(student=student, competition=competition)
        return application
    except Applications.DoesNotExist:
        return False


class MainView(LoginRequiredMixin, View):
    login_url = 'log_user_url'

    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            competitions = Competitions.objects.filter(Q(description__icontains=search_query) | Q(company__description__icontains=search_query) | Q(company__name__icontains=search_query))
        else:
            competitions = Competitions.objects.all()

        check_dates(competitions)
        return render(self.request, "oil_grants/home.html", context={'competitions': competitions, })


class CompetitionDetailView(LoginRequiredMixin, View):
    login_url = 'log_user_url'

    def post(self, request, id):
        return redirect('add_application_url', id=id)

    def get(self, request, id):
        competition = get_object_or_404(Competitions, id=id)
        check_dates([competition])

        application = get_or_pass(request.user, competition)
        return render(self.request, "oil_grants/competition_detail.html", context={'competition': competition,
                                                                                   'application': application})


class ContractDetailView(LoginRequiredMixin, View):
    login_url = 'log_user_url'

    def get(self, request, id):
        contract = get_object_or_404(Contract, id=id)
        if contract.student == request.user:
            return render(self.request, "oil_grants/contract_detail.html", context={'contract': contract, })
        else:
            return HttpResponseForbidden()


class AddApplicationView(LoginRequiredMixin, View):
    login_url = 'log_user_url'

    def post(self, request, id):
        if request.POST.get("yes"):
            competition = get_object_or_404(Competitions, id=id)
            if competition.status != "ended" and competition.status != "didn't start":
                application = Applications.objects.create(student=request.user,
                                                          competition=competition, )
                return render(self.request, "oil_grants/competition_detail.html", context={'competition': competition,
                                                                                           'application': application})
            else:
                return HttpResponseBadRequest()

        return redirect('competition_detail_url', id=id)

    def get(self, request, id):
        competition = get_object_or_404(Competitions, id=id)
        return render(self.request, "oil_grants/confirm_application.html", context={'competition': competition, })
