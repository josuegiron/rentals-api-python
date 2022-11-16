from django.urls import path
from users import views

urlpatterns = [
    path('tokens/', views.GenerateToken.as_view()),
    path('login/', views.LoginUser.as_view()),

    # Search
    path('search/', views.SearchView.as_view({'get': 'list', 'post': 'create'})),
    path('search/<str:pk>/', views.SearchView.as_view({'get': 'retrieve'})),
    
    # User
    path('', views.UserView.as_view({'get': 'list', 'post': 'create'})),
    path('<str:pk>/', views.UserView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]
