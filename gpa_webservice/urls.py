from django.urls import path
from gpa_webservice.views import SignUpView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register')
]