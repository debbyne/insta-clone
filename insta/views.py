from django.shortcuts import render
from django.http  import HttpResponse
from .models import Post,Profile
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    post = Post.objects.all()
    return render(request, 'index.html')

@login_required(login_url='/accounts/login')
def search_results(request):

    if 'search_username' in request.GET and request.GET["search_username"]:
        search_term = request.GET.get("search_username")
        searched_username = Profile.search_profile(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message, 'profile':searched_username})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

