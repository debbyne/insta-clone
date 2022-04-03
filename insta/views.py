from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse,HttpResponseRedirect
from .models import Post,Profile,Comments,Follow
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UpdateUserForm, UpdateUserProfileForm, PostForm, CommentsForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


# Create your views here.

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

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'django_registration/signup.html', {'form': form})

@login_required(login_url='/accounts/login')
def index(request):
    images = Post.objects.all()
    user = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    return render(request, 'index.html', {'images': images,'form': form,'user': user,})
