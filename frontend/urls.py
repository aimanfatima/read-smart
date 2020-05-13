from django.urls import path
from .views import (
    homepage,
    doc_view,
    pdf_view
)

urlpatterns = [
    path("", homepage),
    path("show_doc/", doc_view), 
    path("read_pdf/", pdf_view)
]