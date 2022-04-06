from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'insta'

urlpatterns=[
    path('',views.index,name = 'index'),
    path('search/', views.search_results, name='search_results'),
    path('profile/', views.profile, name='profile'),
    path('userProfile/<username>/', views.userProfile, name='userProfile'),
    re_path(r'^newPostForm/$', views.newPostForm, name='newPostForm'),
    re_path(r'^welcome/$', views.welcome, name='welcome'),
]   
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
   