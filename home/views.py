from django.shortcuts import render

# Create your views here.


def index(request):
    """
    A view to return index page
    """
    print("about to render...")
    
    return render(
        request,
        "home/index.html"
    )