from django.conf.urls import url,include
from django.urls import path,re_path
from . import views

urlpatterns = (
    #url(r'^(?i)login/$', views.showLoginPage, name='login'),
    #path('test', views.test),
    #path('', views.Index),
    
    #path('mainstore/', views.mainstorehome, name='mainstore'),
    #path('mislipview/', views.mislipview, name='mislipview'),

    #path('mislips/', views.ajax_mislips, name='ajax_mislips'),
    
    path('ajax/getcurrentyear', views.getcurrentyear, name='getcurrentyear'),
    path('ajax/pos', views.pos, name='pos'),
    path('ajax/poedit/<str:finyear>/<int:poid>/', views.poedit, name='poedit'),
    path('ajax/pocreate/<str:finyear>/<int:poid>/', views.pocreate, name='pocreate'),
    path('ajax/podel/<int:poid>/', views.podel, name='podel'),
    path('ajax/poprint/<int:poid>/', views.poprint, name='poprint'),
    path('ajax/poamendmentprint/', views.poamendmentprint, name='poamendmentprint'),
    path('ajax/poauth/<int:poid>/', views.poauth, name='poauth'),

    path('ajax/poitems', views.poitems, name='poitems'),
    path('ajax/poitemedit/<int:poid>/<str:stockno>/', views.poitemedit, name='poitemedit'),
    path('ajax/poitemcreate/<int:poid>/<str:stockno>/', views.poitemcreate, name='poitemcreate'),
    path('ajax/poitemdel/<int:poid>/<str:stockno>/', views.poitemdel, name='poitemdel'),
    path('ajax/mpritems/', views.mpr_items, name='mpritems'),

    path('ajax/poamendments', views.poamendments, name='poamendments'),
    path('ajax/poamendmentsedit/<int:poid>/<str:stockno>/', views.poamendmentsedit, name='poamendmentsedit'),
    path('ajax/poamendmentscreate/<int:poid>/<str:stockno>/', views.poamendmentscreate, name='poamendmentscreate'),
    path('ajax/poamendmentsdel/<int:poid>/<str:stockno>/', views.poamendmentsdel, name='poamendmentsdel'),

    path('ajax/pomprs', views.pomprs, name='pomprs'),
    path('ajax/pompredit/<int:poid>/<str:mprno>/', views.pompredit, name='pompredit'),
    path('ajax/pomprcreate/<int:poid>/<str:mprno>/', views.pomprcreate, name='pomprcreate'),
    path('ajax/pomprdel/<int:poid>/<str:mprno>/', views.pomprdel, name='pomprdel'),

    path('ajax/amendpo/', views.amend_po, name='amendpo'),



)