from django.urls import path
from properties import views

urlpatterns = [
    # PropertyType
    path('property_types/', views.PropertyTypeView.as_view({'get': 'list', 'post': 'create'})),
    path('property_types/<str:pk>/', views.PropertyTypeView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # Plan
    path('plans/', views.PlanView.as_view({'get': 'list', 'post': 'create'})),
    path('plans/<str:pk>/', views.PlanView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # AreaType
    path('area_types/', views.AreaTypeView.as_view({'get': 'list', 'post': 'create'})),
    path('area_types/<str:pk>/', views.AreaTypeView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # Amenity
    path('amenities/', views.AmenityView.as_view({'get': 'list', 'post': 'create'})),
    path('amenities/<str:pk>/', views.AmenityView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # Area
    path('areas/', views.AreaView.as_view({'get': 'list', 'post': 'create'})),
    path('areas/<str:pk>/', views.AreaView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # AreaImage
    path('area_images/', views.AreaImageView.as_view({'get': 'list', 'post': 'create'})),
    path('area_images/<str:pk>/', views.AreaImageView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # AreaReservation 
    path('area_reservations/', views.AreaReservationView.as_view({'get': 'list', 'post': 'create'})),
    path('area_reservations/<str:pk>/', views.AreaReservationView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # Showing
    path('showings/', views.ShowingView.as_view({'get': 'list', 'post': 'create'})),
    path('showings/<str:pk>/', views.ShowingView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # Property
    path('', views.PropertyView.as_view({'get': 'list', 'post': 'create'})),
    path('<str:pk>/', views.PropertyView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

]
