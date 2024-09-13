from django.shortcuts import render, redirect
from newsapi import NewsApiClient

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def index(request):
    newsapi = NewsApiClient(api_key='69c4680460cd4b81ad49bdc98849ebc3')
    top= newsapi.get_top_headlines(sources='techradar')
    my_articles= top['articles']
    news=[]
    desc=[]
    img=[]
    dates = []
    sources = []
    for i in range(len(my_articles)):
        f=my_articles[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        dates.append(f['publishedAt'])
        sources.append(f['source']['name'])
        mylist=zip(news,desc,img, dates, sources)
    return render(request,'index.html',context={'mylist':mylist})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            messages.success(request, 'Signup successful!')  # Add success message
            return redirect('index')  # Redirect to index page after successful sign-up
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to index after successful login
        else:
            return render(request, 'signin.html', {'error': 'Invalid login credentials'})
    return render(request, 'signin.html')

def about(request):
    return HttpResponse("About Us")

def contact(request):
    return HttpResponse("Contact Us")

def news(request):
    return HttpResponse("News")


