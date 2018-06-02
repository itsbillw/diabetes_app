from django.shortcuts import render

def index(request):
    """The home page for Learning Log."""
    return render(request, 'diabetes_app/index.html')

def info(request):
    """The info page for Learning Log."""
    return render(request, 'diabetes_app/info.html')