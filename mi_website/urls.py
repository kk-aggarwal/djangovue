from django.conf.urls import url,include
from django.urls import path,re_path
from . import views

urlpatterns = (
    #url(r'^(?i)login/$', views.showLoginPage, name='login'),
    path('test', views.test),
    path('', views.Index),
    path('mainstore/', views.mainstorehome, name='mainstore'),
    path('mislipview/', views.mislipview, name='mislipview'),

    path('mislips/', views.ajax_mislips, name='ajax_mislips'),
    path('ajax/mislipedit/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:mislipdate>', views.mislipedit, name='mislipedit'),
    path('ajax/mislipdel/<str:finyear>/<int:mislipno>/<int:matgrp>', views.mislipdel, name='mislipdel'),
    path('ajax/mislipprint/<str:finyear>/<int:mislipno>/<int:matgrp>', views.mislipprint, name='mislipprint'),

    path('ajax/mislipcreate/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:mislipdate>', views.mislipcreate, name='mislipcreate'),
    path('ajax/getsuppaddfrompono/', views.getsuppaddfrompono, name='getsuppaddfrompono'),

    path('mislipitems/', views.ajax_mislipitems, name='mislipitems'),
    path('ajax/mislipitemedit/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:stockno>', views.mislipitemedit, name='mislipitemedit'),
    path('ajax/mislipitemdel/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:stockno>', views.mislipitemdel, name='mislipitemdel'),

    path('ajax/mislipitemcreate/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:stockno>', views.mislipitemcreate, name='mislipitemcreate'),
    path('ajax/getstocknodes/', views.getdesfromstockno, name='getstocknodes'),

    path('mislipmrrs/', views.ajax_mislipmrrs, name='mislipmrrs'),
    path('ajax/mislipmrredit/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:mrrno>', views.mislipmrredit,
         name='mislipmrredit'),
    path('ajax/mislipmrrdel/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:mrrno>', views.mislipmrrdel,
         name='mislipmrrdel'),

    path('ajax/mislipmrrcreate/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:mrrno>', views.mislipmrrcreate,
         name='mislipmrrcreate'),

    path('mislipbills/', views.ajax_mislipbills, name='mislipbills'),
    path('ajax/mislipbilledit/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:billno>/<str:billtype>', views.mislipbilledit,
         name='mislipbilledit'),
    path('ajax/mislipbilldel/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:billno>/<str:billtype>', views.mislipbilldel,
         name='mislipbilldel'),

    path('ajax/mislipbillcreate/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:billno>/<str:billtype>', views.mislipbillcreate,
         name='mislipbillcreate'),

    path('mrrview/', views.mrrview, name='mrrview'),
    path('mrrs/', views.ajax_mrrs, name='ajax_mrrs'),
    path('ajax/mrredit/<str:finyear>/<int:mrrno>/<str:mrrdate>', views.mrredit, name='mrredit'),
    path('ajax/mrrdel/<str:finyear>/<int:mrrno>/', views.mrrdel, name='mrrdel'),
    path('ajax/mrrcreate/<str:finyear>/<int:mrrno>/<str:mrrdate>', views.mrrcreate, name='mrrcreate'),

    path('mrrvalues/', views.ajax_mrrvalues, name='mrrvalues'),
    path('ajax/mrrvalueedit/<str:finyear>/<int:mrrno>/<str:billno>', views.mrrvalueedit, name='mrrvalueedit'),
    path('ajax/mrrvaluedel/<str:finyear>/<int:mrrno>/<str:billno>', views.mrrvaluedel, name='mrrvaluedel'),
    path('ajax/mrrvaluecreate/<str:finyear>/<int:mrrno>/<str:billno>', views.mrrvaluecreate, name='mrrvaluecreate'),

    path('ledgerview/', views.ledgerview, name='ledgerview'),
    path('ledger/', views.ajax_ledger, name='ajax_ledger'),
    path('ajax/ledgeredit/<str:finyear>/<str:stockno>/<int:matgroup>/<str:transid>', views.ledgeredit, name='ledgeredit'),
    path('ajax/ledgerdel/<str:transid>/', views.ledgerdel, name='ledgerdel'),
    path('ajax/ledgercreate/<str:finyear>/<str:stockno>/<int:matgroup>/<str:transid>/', views.ledgercreate, name='ledgercreate'),

    path('ajax/updatewon/', views.updateWON,name='updatewon'),

    path('stmislipsview/', views.stmislipsview, name='stmislipsview'),

    path('stdocregisterview/', views.stdocregisterview, name='stdocregisterview'),
    path('ajax/stdocregister/', views.ajax_stdocregister, name='ajax_stdocregister'),
    path('ajax/stdocregisteredit/<str:yearid>/<int:groupid>/<int:docno>/<int:doctype>', views.stdocregisteredit, name='stdocregisteredit'),
    path('ajax/stdocregisterdel/<str:yearid>/<int:groupid>/<int:docno>/<int:doctype>', views.stdocregisterdel, name='stdocregisterdel'),
    path('ajax/stdocregistercreate/<str:yearid>/<int:groupid>/<int:docno>/<int:doctype>', views.stdocregistercreate, name='stdocregistercreate'),
    path('ajax/stdocledger/', views.ajax_stdocledger, name='ajax_stdocledger'),

    path('stmislipsview/', views.stmislipsview, name='stmislipsview'),
    path('ajax/stmislips/', views.ajax_stmislips, name='ajax_stmislips'),
    path('ajax/stmislipedit/<str:finyear>/<int:mislipno>/<int:matgrp>/<str:mislipdate>', views.stmislipedit,
         name='stmislipedit'),

    path('ajax/stmislipitems/', views.ajax_stmislipitems, name='ajax_stmislipitems'),
    path('ajax/stmislipitemsedit/<str:yearid>/<int:docref>/<str:stockno>', views.stmislipitemsedit, name='stmislipitemsedit'),
    path('ajax/stmislipitemsdel/<str:yearid>/<int:groupid>/<int:docno>/<int:doctype>', views.stmislipitemsdel, name='stmislipitemsdel'),
    path('ajax/stmislipitemscreate/<str:yearid>/<int:groupid>/<int:docno>/<int:doctype>', views.stmislipitemscreate, name='stmislipitemscreate'),

    path('ststockmasterview/', views.ststockmasterview, name='ststockmasterview'),
    path('ajax/ststockmaster/', views.ajax_ststockmaster, name='ajax_ststockmaster'),
    path('ajax/ststockmasteredit/<str:stockno>', views.ststockmasteredit, name='ststockmasteredit'),
    path('ajax/ststockmasterdel/<str:stockno>', views.ststockmasterdel, name='ststockmasterdel'),
    path('ajax/ststockmastercreate/<str:stockno>', views.ststockmastercreate, name='ststockmastercreate'),

    path('ajax/getcurrentyear', views.getcurrentyear, name='getcurrentyear'),
    path('ajax/getmatgroups', views.getmatgroups, name='getmatgroups'),




)
