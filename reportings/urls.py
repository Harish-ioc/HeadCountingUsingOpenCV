from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('datacam/<int:ids>', views.datacam),
    path('nums/', views.nums),
    path('insight/', views.resultDashboard),
    path('getudate/', views.customDashBoard),
    path('teachers/<str:name>', views.teachers),
]