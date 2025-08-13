
from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    # post method and also work get method
    path('details', DetailsView.as_view(), name='details'),
    # delete
    path('details/<int:id>', DetailsDeleteView.as_view(), name='details-delete'),
    # single value view page
    path('details/signle/<int:id>', DetailView.as_view(), name='detail'), 
    # search
    path('search/invoice', InvoiceSearchView.as_view(), name='invoice-search'), 
    
]