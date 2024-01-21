from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from reviews.forms import ReviewForm
from wishlist.models import Wishlist
from transactions.models import Transaction
from django.contrib.auth.decorators import login_required

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    is_wished = Wishlist.objects.filter(user=request.user, book=book).exists()
    transaction = Transaction.objects.filter(user=request.user, book=book, is_returned=False).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book-detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'details.html', {'form': form,'book': book,'is_wished': is_wished,'transaction':transaction})
