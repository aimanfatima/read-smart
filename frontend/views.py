from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from docx import Document
from .utils import doc_to_pdf_converter
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