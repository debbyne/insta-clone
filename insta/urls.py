from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name = 'index'),
    path('search/', views.search_results, name='search_results'),
    path('profile/', views.profile, name='profile'),
    path('userProfile/<username>/', views.userProfile, name='userProfile'),

]   
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
   