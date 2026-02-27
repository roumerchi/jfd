from django.urls import path

from .views import *

urlpatterns = [
    path('api/contacts/', ContactsApiView.as_view(), name='contacts'), # get | post
    path('api/contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact'), # get | put | delete
]

