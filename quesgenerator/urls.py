from django.urls import path
from .views import (
    GetFillUps,
)

urlpatterns = [
    path("get_fill_ups/", GetFillUps.as_view()),
]