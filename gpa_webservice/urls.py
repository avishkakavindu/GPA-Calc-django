from django.urls import path
from gpa_webservice.views import SignUpView, UserActivationView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>', UserActivationView.as_view(), name='user_activation'),
    path('activate/<str:uidb64>/<str:token>', UserActivationView.as_view(), name='user_activation'),
]