from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from docx import Document
from .utils import doc_to_pdf_converter, pdfparser
import requests
import json

def homepage(request):
    context = {
        
    }
    return render(request, 'home_page.html', context=context)

@api_view(['GET', 'POST'])
@csrf_exempt 
def doc_view(request):
    if request.method == "POST":
        try:
            file = request.FILES["file"]
            print(file.content_type)
        except KeyError:
            return Response(
                {"message": "File not uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )
        if file.content_type != "application/msword" and file.content_type != "application/ms-doc" and file.content_type != "application/doc" and file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return Response(
                {"message": "File type not supported"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        ## DO SOMETHING WITH FILE ##
        print(file)
        doc_path = 'static/doc_file.docx'
        pdf_path = 'static/pdf_file.pdf'
        with open(doc_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        document = Document(doc_path)
        fullText = []
        questions = []
        for para in document.paragraphs:
            if len(para.text) != 0:
                fullText.append(para.text)
            #         questions.append(json_response)
        #############################
        doc_to_pdf_converter(doc_path)
        context = {
            'doc_path' : doc_path,
            'pdf_path': pdf_path,
            'no_of_para': len(fullText),
            'full_text': fullText,
            'full_text_json': json.dumps(fullText),
            # 'questions': questions
        }
        return render(request, 'doc_view.html', context=context, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@csrf_exempt
def pdf_view(request):
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
        filename = default_storage.save("static/uploaded_file.pdf",file)
        uploaded_file_url = default_storage.url(filename)

        # pdf = fitz.open(uploaded_file_url)
        # print ("number of pages:", pdf.pageCount)
        text_page_wise = pdfparser(uploaded_file_url)
        print(type(text_page_wise))
        print(type(text_page_wise[0]))
        print(filename)
        # questions_page_wise = get_questions_page_wise(text_page_wise)
        ##############################
        context = {
            'filename':filename.split("static/",1)[1],
            'no_of_pages': len(text_page_wise), 
            'text_page_wise': text_page_wise,
            'text_page_wise_json': json.dumps(text_page_wise)
            # 'questions_page_wise': questions_page_wise
        }
        return render(request, 'pdf_view.html', context=context, status=status.HTTP_201_CREATED)