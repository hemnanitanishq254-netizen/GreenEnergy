from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('create/', views.create_listing, name='create_listing'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:pk>/update/', views.update_listing, name='update_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
]