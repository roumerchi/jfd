from django.urls import path

from contacts.views import ContactsPageView

urlpatterns = [
    # by default, for convenience the main page, since it is no longer required
    path('', ContactsPageView.as_view(), name='contacts_page') # 'contacts/'
]
