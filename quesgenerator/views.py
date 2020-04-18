from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse
from quesgenerator.services.get_fill_in_the_blanks import Article

# Create your views here.
class GetFillUps(APIView):
    def get(self, request):
        data = request.data
        if ("text" not in data) or len(data["text"]) == 0:
            return Response(
                {"message": "Text is missing"}, status=status.HTTP_404_NOT_FOUND
            )
        article = Article(data["text"])
        fill_ups = article.generate_trivia_sentences()
        fill_up_response = {
            'data': data,
            'fill_ups':fill_ups
        }
        return Response(fill_up_response , status=status.HTTP_200_OK)