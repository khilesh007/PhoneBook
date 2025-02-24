from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import register, login, mark_as_spam, search_by_name, search_by_phone_number, get_contacts, add_contact

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('mark_as_spam/', mark_as_spam, name='mark_as_spam'),
    path('search-by-name/', search_by_name, name='search_by_name'),
    path('search-by-phone/', search_by_phone_number, name='search_by_phone_number'),
    path('add-contact/', add_contact, name='add_contact'),
    path('get-contacts/', get_contacts, name='get_contacts'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


