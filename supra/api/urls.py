from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()), # get
    path('contacts/', ContactsApiView.as_view(), name='contacts'), # get | post
    path('contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact'), # get | put | delete
]
