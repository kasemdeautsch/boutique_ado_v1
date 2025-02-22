from django.shortcuts import render

# Create your views here.


def index(request):
    print("about to render...")
    return render(
        request,
        "home/index.html"
    )