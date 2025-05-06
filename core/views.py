from django.shortcuts import render


def home_page(request):
    context = {}
    return render(request, 'base.html', context)
# Create your views here.
def main_page(request):
    context = {}
    return render(request, 'main.html', context)