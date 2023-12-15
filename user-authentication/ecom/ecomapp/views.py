from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
def index(request):
    return render(request,"index.html")

def up_events(request):
    return render(request,"index.html")

def about(request):
    return render(request,"index.html")

def contact(request):
    return render(request,"index.html")
    
def up_events(request):
    return render(request,"index.html")

def team(request):
    return render(request,"index.html")

def batch(request):
    return render(request,"index.html")
