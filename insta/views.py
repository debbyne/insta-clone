from django.shortcuts import render
from django.http  import HttpResponse
from .models import Images
from .email import send_welcome_email

# Create your views here.
def index(request):
    images = Images.get_images()
    title= 'Photo Display'
    return render(request, 'all-photos/pictures.html', {"images":images, "title":title})

# def welcome_email(request):
#     if request.method == 'POST':
#         form = (request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['your_name']
#             email = form.cleaned_data['email']

#             recipient = NewsLetterRecipients(name = name,email =email)
#             recipient.save()
#             send_welcome_email(name,email)

#             HttpResponseRedirect('news_today')
#             #.................
#     return render(request, 'email/welcome-email.html', {"date": date,"news":news,"letterForm":form})