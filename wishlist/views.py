from django.shortcuts import render, get_object_or_404, redirect
from .models import Wishlist
from catalog.models import Book
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist_view.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    Wishlist.objects.create(user=request.user, book=book)
    return redirect('home')

@login_required
def remove_from_wishlist(request, book_id):
    Wishlist.objects.filter(user=request.user, book_id=book_id).delete()
    return redirect('home')
