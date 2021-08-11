from django.urls import path
from . import views


urlpatterns = [
    path('', views.studentRating, name="student rating page"),
]
