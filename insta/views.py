from inspect import Parameter
from pickle import FALSE
from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Post,Profile,Comments,Follow
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UpdateUserForm, UpdateUserProfileForm, PostForm, CommentsForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


#Create your views here.

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
    return render(request, 'django_registration/registration_form.html', {'form': form})

@login_required(login_url='login')
def logoutrequest(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("social:homepage")

def loginrequest(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"loginform": form})

@login_required(login_url='/accounts/login')
def index(request):
    images = Post.objects.all()
    user = User.objects.exclude(id=request.user.id)
    # if request.method == 'POST':
    #     form = PostForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.user = request.user.profile
    #         post.save()
    #         return HttpResponseRedirect(request.path_info)
    # else:
    #     form = PostForm()
    return render(request, 'index.html', {'images': images,'user': user})

@login_required(login_url='login')
def profile(request):
    images = request.user.profile.posts.all()
    profile = request.user
    profileForm = UpdateUserProfileForm()
    if request.method == 'POST':
        profileForm = UpdateUserProfileForm(request.POST, request.FILES)
        if profileForm.is_valid():
            profile=profileForm.save(commit=FALSE)
            profile.save()
        else:
           
            profileForm = UpdateUserProfileForm()

        
    return render(request, 'profile.html' ,{'user': profile, 'profileForm':profileForm})

@login_required(login_url='login')
def userProfile(request, username):
    userProfile = request.user
    if request.user == userProfile:
        return redirect('profile', username=request.user.username)
    user_posts = userProfile.profile.posts.all()
    users = User.objects.get(username=username)
    total_followers = len(Follow.objects.total_followers(users))
    total_following = len(Follow.objects.total_following(users))
    follow_status = None
    Parameters = {
        'userProfile': userProfile,
        'user_posts': user_posts,
        'followers': total_followers,
        'following': total_following,
        'follow_status': follow_status,
    }
    return render(request, 'userprofile.html', Parameters)

def follow(request, follow):
       if request.method == 'GET':
        userProfile = Profile.objects.get(pk=follow)
        follow_s = Follow(follower=request.user.profile, followed=userProfile)
        follow_s.save()
        return redirect('userProfile', userProfile.user.username)

def unfollow(request, unfollow):
      if request.method == 'GET':
        userProfile = Profile.objects.get(pk=unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=userProfile)
        unfollow_d.delete()
        return redirect('userProfile', userProfile.user.username)


def likePost(request):
    image = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        image.likes.remove(request.user)
        is_liked = False
    else:
        image.likes.add(request.user)
        is_liked = False

        Parameters = {
        'image': image,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    if request.is_ajax():
        html = render_to_string('postlikes.html', Parameters, request=request)
        return JsonResponse({'form': html})

@login_required(login_url='login')
def postComments(request, id):
    image = get_object_or_404(Post, pk=id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentsForm()
    Parameters = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'photos.html', Parameters)

@login_required(login_url='login')
def newPostForm(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            user = current_user
            image.save()
            
        return redirect('index')

    else:
        form = PostForm()
    return render(request, 'newpost.html', {"form": form})

@login_required(login_url='login')
def welcome(request):
    return render(request, 'welcome.html')
