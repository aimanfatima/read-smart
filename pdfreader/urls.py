from django.urls import path
from .views import (
    OpenPDF,
)

urlpatterns = [
    path("read_pdf/", OpenPDF.as_view()),
]