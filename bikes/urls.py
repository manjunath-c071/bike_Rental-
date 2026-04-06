from django.urls import path
from . import views

app_name = 'bikes'

urlpatterns = [
    path('', views.bike_list_view, name='bike_list'),
    path('<int:bike_id>/', views.bike_detail_view, name='bike_detail'),
]
