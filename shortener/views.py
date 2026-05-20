import secrets
from django.shortcuts import render, redirect, get_object_or_404
from .models import URL

# Create your views here.
def index(request):
    if request.method == "POST":
        given_url = request.POST["given_url"]
        if not given_url.startswith(('http://', 'https://')):
            given_url = 'https://' + given_url
        random = secrets.token_urlsafe(6)
        url = URL.objects.create(original_url = given_url, short_code = random)
        return redirect("shortener:index")
    all_urls = URL.objects.all()
    context = {
        "all_urls": all_urls
    }
    return render(request, "shortener/index.html", context)

def redirecting(request, short_codes):
    if request.method == "GET":
        original_object = get_object_or_404(URL, short_code = short_codes)
    return redirect(original_object.original_url)

def delete(request, object_id):
    if request.method == "POST":
        deleting_object = get_object_or_404(URL, pk=object_id)
        deleting_object.delete()
    return redirect("shortener:index")