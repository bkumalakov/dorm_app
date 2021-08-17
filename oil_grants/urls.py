from django.urls import path
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name="main_url"),
    path('competition/<int:id>/', CompetitionDetailView.as_view(), name="competition_detail_url"),
    path('competition/<int:id>/submit/', AddApplicationView.as_view(), name="add_application_url"),
    path('contract/<int:id>/', ContractDetailView.as_view(), name="contract_detail_url"),

]
