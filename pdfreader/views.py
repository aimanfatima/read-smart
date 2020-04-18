# import PyPDF2
# import fitz
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from .utils import pdfparser, get_questions_page_wise


# Create your views here.
class OpenPDF(APIView):
    def post(self, request):
        try:
            file = request.FILES["file"]
            print(file.content_type)
        except KeyError:
            return Response(
                {"message": "File not uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )
        if file.content_type != "application/pdf":
            return Response(
                {"message": "File type not supported"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        ## DO SOMETHING WITH FILE ##
        filename = default_storage.save("pdfreader/static/uploaded_file.pdf",file)
        uploaded_file_url = default_storage.url(filename)

        # pdf = fitz.open(uploaded_file_url)
        # print ("number of pages:", pdf.pageCount)
        text_page_wise = pdfparser(uploaded_file_url)
        print(type(text_page_wise))

        questions_page_wise = get_questions_page_wise(text_page_wise)
        ##############################
        context = {
            'filename':filename.split("/static/",1)[1],
            'no_of_pages': len(text_page_wise), 
            'text_page_wise': text_page_wise,
            'questions_page_wise': questions_page_wise
        }
        return render(request, 'pdf_view.html', context=context, status=status.HTTP_201_CREATED)