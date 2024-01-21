from django.db import models
from categories.models import Categories

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    publication_date = models.DateField()
    genre = models.CharField(max_length=100)
    availability_status = models.BooleanField(default=True)
    number_of_copies = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True, blank=True)
    image = models.ImageField(
        upload_to="catalog/media/uploads",
        height_field=None,
        width_field=None,
        max_length=None,
        default="",
    )
    
    def __str__(self):
        return self.title
