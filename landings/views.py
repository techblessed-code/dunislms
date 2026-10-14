from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')


def blog(request):
    return JsonResponse({'message': 'blog page - Coming Soon'})
