from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from reviews.forms import ReviewForm

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
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
    return render(request, 'details.html', {'form': form,'book': book})
