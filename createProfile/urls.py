from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getKeywords/', views.getKeywords),
    path('viewProfile/', views.viewProfile),
    path('summary/', views.summary)
]
