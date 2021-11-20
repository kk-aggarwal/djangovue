from django.urls import path
from . import views

urlpatterns = (
    #path('', views.Index),
    path('ajax/balancehom/', views.HomTransacDet, name='balancehom'),
    path('ajax/balancebom/', views.balancebom, name='balancebom'),
    path('ajax/searchdatabase/', views.searchdatabase, name='searchdatabase'),
    path('ajax/dailymislipitems/', views.dailymislipitems, name='dailymislipitems'),
    path('ajax/oplayout/', views.oplayout, name='oplayout'),
    path('ajax/prodprogram/', views.prodprogram, name='prodprogram'),
    path('bom/', views.bom, name='bom'),
    path('pendingmislips/', views.pendingMislips, name='pendingmislips'),
    path('ajax/mtp01/', views.mtp01, name='mtp01'),
    path('ajax/mtp09/', views.mtp09, name='mtp09'),
    path('ajax/mtp10/', views.mtp10, name='mtp10'),
    path('ratestockno/', views.ratestockno, name='ratestockno'),
    path('ajax/homiteminfo/', views.homiteminforesults, name='homiteminforesults'),
    path('ajax/stocknodetail/', views.resultspurDetail, name='stocknodetail'),
    path('ajax/dailymrr/', views.resultsDailyMrr, name='dailymrr'),
    path('ajax/systems/', views.systems, name='systems'),
    path('ajax/finddrwgno/', views.resultsfinddrwgno, name='findgrwgno'),

)