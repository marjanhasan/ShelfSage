from django.shortcuts import render
from catalog.models import Book

def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})