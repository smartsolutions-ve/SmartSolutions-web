from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('', views.landing, name='index'),
    path('contacto/', views.contacto_submit, name='contacto_submit'),
]
