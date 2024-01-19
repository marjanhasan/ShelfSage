from django.urls import path
from .views import SignUpView,ActivateAccountView, UserLoginView, UserLogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate/<str:uid64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
]
