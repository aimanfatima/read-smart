from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    context = {
        
    }
    return render(request, 'home_page.html', context=context)