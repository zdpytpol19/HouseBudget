from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, "main_page.html")

