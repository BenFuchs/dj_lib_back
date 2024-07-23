from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', TokenObtainPairView.as_view()),
    path('test', views.test_member),
    path('bookView', views.book_view),
    path('bookView/<int:id>', views.book_view),
    path('register', views.register),
    path('loan/<int:id>', views.loan),
    path('returnBook/<int:id>', views.returnBook),
    path('showLoans', views.showLoans),
    path('logout/', views.logout_view, name='logout'),
    ] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)