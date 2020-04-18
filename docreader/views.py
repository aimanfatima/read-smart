from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from docx import Document
from .utils import doc_to_pdf_converter
import requests
import json

# Create your views here.
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
        doc_path = 'docreader/static/doc_file.docx'
        pdf_path = 'docreader/static/pdf_file.pdf'
        with open(doc_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        document = Document(doc_path)
        fullText = []
        questions = []
        for para in document.paragraphs:
            fullText.append(para.text)
            if len(para.text) != 0:
                print("\n\n This is a Paragraph\n\n")
                print(para.text)
                ques_response = requests.get('https://readex-major-project.herokuapp.com/get_fill_ups/', data={"text":para.text})
                json_response = json.loads(ques_response.text)
                # print(type(json_response['fill_ups'][0]))   
                if ques_response.status_code==201:
                    questions.append(json_response)
        #############################
        doc_to_pdf_converter(doc_path)
        context = {
            'doc_path' : doc_path,
            'pdf_path': pdf_path,
            'full_text': fullText,
            'questions': questions
        }
        return render(request, 'doc_view.html', context=context, status=status.HTTP_201_CREATED)