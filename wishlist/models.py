from django.db import models
from django.contrib.auth.models import User
from catalog.models import Book

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        verbose_name_plural = 'wishlists'

    def __str__(self):
        return f"{self.user.username}'s wishlist"
