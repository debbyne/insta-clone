from inspect import Parameter
from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse,HttpResponseRedirect, JsonResponse
from .models import Post,Profile,Comments,Follow
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UpdateUserForm, UpdateUserProfileForm, PostForm, CommentsForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.template.loader import render_to_string


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
    users_followed = request.user.profile.following.all()
    posts = Post.objects.filter(profile__in=users_followed).order_by('-posted_on')


@login_required(login_url='/accounts/login')
def posts(request):
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
    return render(request, 'photos.html', {'images': images,'form': form,'user': user,})

@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        userForm = UpdateUserForm(request.POST, instance=request.user)
        profileForm = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            return HttpResponseRedirect(request.path_info)

        else:
            userForm = UpdateUserForm(instance=request.user)
            profileForm = UpdateUserProfileForm(instance=request.user.profile)

        Parameters = {
        'userForm': userForm,
        'profileForm': profileForm,
        'images': images,   

    }
    return render(request, 'profile/profile.html', Parameters)

@login_required(login_url='login')
def userProfile(request, username):
    userProfile = get_object_or_404(User, username=username)

    if request.user == userProfile:
        return redirect('profile', username=request.user.username)
    user_posts = userProfile.profile.posts.all()
    users = User.objects.get(username=username)
    followers = len(Follow.objects.followers(users))
    following = len(Follow.objects.following(users))
    follow_status = None
    Parameters = {
        'userProfile': userProfile,
        'user_posts': user_posts,
        'followers': followers,
        'following': following,
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