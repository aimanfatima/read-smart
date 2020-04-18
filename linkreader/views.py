from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def link_view(request):
    if request.method=="POST":
        context = {
            "link": request.POST['link']
        }
        return render(request, 'link_view.html', context=context)