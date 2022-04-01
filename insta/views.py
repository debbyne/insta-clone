from django.shortcuts import render
from django.http  import HttpResponse
from .models import Images

# Create your views here.
def index(request):
    images = Images.get_images()
    title= 'Photo Display'
    return render(request, 'all-photos/pictures.html', {"images":images, "title":title})
