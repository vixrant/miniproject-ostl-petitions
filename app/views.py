from django.shortcuts import render
from  .models import Petition

def index(request):
    petition_list = Petition.objects.all()
    return render(request, 'index.html', {
        "petition_list": petition_list
    })
