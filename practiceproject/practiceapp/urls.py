from django.urls import path, include
from . import views

urlpatterns = [
    path('student/', views.student_view),
    path('order/', views.order_view)

]