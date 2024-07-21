from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.index),
    path('login/', TokenObtainPairView.as_view()),
    path('test', views.test_member),
    path('bookView', views.book_view),
    path('bookView/<int:id>', views.book_view),
]
