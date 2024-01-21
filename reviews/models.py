from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book
from django.core.validators import MaxValueValidator, MinValueValidator
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='reviews')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.book.title}"
