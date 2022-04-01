from django.shortcuts import render
from django.http  import HttpResponse

# Create your views here.
images = Images.get_images()
    title= 'Thee Dev Gallery'
    return render(request, 'all-photos/pictures.html', {"images":images, "title":title})
