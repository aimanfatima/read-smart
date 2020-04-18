from django.urls import path
from .views import (
    doc_view,
)

urlpatterns = [
    path("show_doc/", doc_view),
]