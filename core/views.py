from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def contacts(request):
    return render(request, 'core/contacts.html')

def about(request):
    return render(request, 'core/about.html')