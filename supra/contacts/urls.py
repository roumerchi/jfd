from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # get
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # post
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), # post
    path('contacts/', ContactsApiView.as_view(), name='contacts'), # get | post
    path('contacts/bulk/', ContactsBulkImportApiView.as_view(), name='contacts_bulk'), # get
    path('contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact'), # get | put | delete
    path('weather/', CityWeatherAPIView.as_view(), name='city-weather'), # get
]
