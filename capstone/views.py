from django.shortcuts import render,redirect

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    return render(request, 'all-capstone/home.html')

def about(request):
    return render(request, 'all-capstone/about.html')
