from django.urls import path
from . import views
urlpatterns = (
    path('', views.Index),
    path('ajax/wgps/', views.ajax_wgps, name='ajax_wgps'),
    

)