from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def main(request):
    return render(request, 'tape/index.html')
