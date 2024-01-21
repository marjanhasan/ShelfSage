from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:book_id>/', views.add_review, name='add_review'),
    # Add more URLs as needed for edit, delete, list views
]
