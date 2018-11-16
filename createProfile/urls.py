from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getKeywords/', views.getKeywords),
    path('editProfiles/', views.editProfiles)
]
