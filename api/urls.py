from django.urls import path
from api import views

urlpatterns = [
    path('',views.StudentCreate.as_view()),
]