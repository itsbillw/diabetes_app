from django.shortcuts import render

def index(request):
    """The home page for Learning Log."""
    return render(request, 'diabetes_app/index.html')
