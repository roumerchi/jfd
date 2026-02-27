from django.urls import path

from .views import *

urlpatterns = [
    path('contacts/', ContactsApiView.as_view(), name='contacts'), # get | post
    path('contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact'), # get | put | delete
]

