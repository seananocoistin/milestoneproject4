from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_listings, name='listings'),
    path('<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('add/', views.add_listing, name='add_listing'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('edit/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('delete/<int:listing_id>/', views.delete_listing, name='delete_listing'),
]
