from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from catalog.models import Book
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from reviews.models import Review
from reviews.forms import ReviewForm

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.availability_status and book.number_of_copies > 0:
        Transaction.objects.create(user=request.user, book=book)
        book.number_of_copies -= 1
        if book.number_of_copies == 0:
            book.availability_status = False
        book.save()
    else:
        messages.error(request, "Document deleted.")
    return redirect('book-detail', pk=book_id)


@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id, user=request.user)
    book = transaction.book
    review_form = ReviewForm(request.POST or None)

    if request.method == 'POST' and review_form.is_valid():
        # Return the book
        transaction.is_returned = True
        transaction.returned_date = timezone.now()
        transaction.save()

        # Update the book availability
        book.number_of_copies += 1
        book.availability_status = True
        book.save()

        # Create a review
        Review.objects.create(
            user=request.user,
            book=book,
            rating=review_form.cleaned_data['rating'],
            content=review_form.cleaned_data['content']
        )

        return redirect('book-detail', pk=book.pk)
    
    context = {
        'transaction': transaction,
        'book': book,
        'review_form': review_form,
    }
    return render(request, 'return_book.html', context)

