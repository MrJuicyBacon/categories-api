from django.urls import path
from . import views


urlpatterns = [
    path(r'categories/<int:pk>/', views.CategoryRetrieveView.as_view()),
]
