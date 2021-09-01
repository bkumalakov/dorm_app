from django.urls import path
from .views import *
from .decorators import check_recaptcha

urlpatterns = [
    path('', MainView.as_view(), name="main_url"),
    path('competition/<str:competition_number>/', CompetitionDetailView.as_view(), name="competition_detail_url"),
    path('applications/', ApplicationListView.as_view(), name='applications_url'),
    path('application/<str:competition_number>/submit/',  check_recaptcha(AddApplicationView.as_view()), name="add_application_url"),
    path('application/<int:id>/delete/', check_recaptcha(DeleteApplicationView.as_view()), name="delete_application_url"),
    # path('contract/<int:id>/', ContractDetailView.as_view(), name="contract_detail_url"),

]
