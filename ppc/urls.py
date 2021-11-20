from django.urls import path
from . import views

urlpatterns = (
    path('', views.Index),
    path('ajax/workordernos/', views.ajax_workordernos, name='ajax_workordernos'),
    path('ajax/shortagelists/', views.ajax_shortagelists, name='ajax_shortagelists'),
    path('ajax/parentsec/', views.ajax_parentsec, name='ajax_parentsec'),
    path('ajax/orderlist/', views.ajax_orderlist, name='ajax_orderlist'),
    path('ajax/shortagelist/', views.ajax_shortagelist, name='ajax_shortagelist'),
    path('ajax/smallpartsrunning/', views.ajax_smallparts_running, name='ajax_smallparts_running'),
    path('ajax/homtransac/', views.ajax_hom_transac, name='ajax_hom_transac'),
    path('ajax/operations/', views.ajax_operations, name='ajax_operations'),
    path('operationcreate/', views.operationcreate, name='operationcreate'),
    path('olitempdcupdate/', views.olitempdcupdate, name='olitempdcupdate'),
    path('olitemremarksupdate/', views.olitemremarksupdate, name='olitemremarksupdate'),
)