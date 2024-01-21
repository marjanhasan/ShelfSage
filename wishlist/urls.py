from django.urls import path
from .views import wishlist_view, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('', wishlist_view, name='wishlist_view'),
    path('add/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:book_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
