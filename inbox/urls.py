
from django.urls import path
from inbox import views

urlpatterns = [
    # Attachments
    path('attachments/', views.AttachmentView.as_view({'get': 'list', 'post': 'create'})),
    path('attachments/<str:pk>/', views.AttachmentView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # Messages
    path('', views.MessageView.as_view({'get': 'list', 'post': 'create'})),
    path('<str:pk>/', views.MessageView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

    # PropertyMessages
    path('properties/<str:pk>/messages/', views.PropertyMessageView.as_view({'get': 'list', 'post': 'create'})),
    path('properties/<str:property>/messages/<str:message>/', views.PropertyMessageView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]
