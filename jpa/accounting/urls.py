from django.conf.urls import url
from django.urls import path
from . import views
#from.views import GeneratePDF

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('message', views.message, name="message"),
    path('corporation', views.corporation, name="corporation"),
    path('vouchersentry', views.vouchersentry, name="vouchersentry"),
    path('tjentry', views.tjentry, name="tjentry"),
    path('ledger', views.ledger, name="ledger"),
    path('tjledger', views.tjledger, name="tjledger"),
    path('credit', views.credit, name="credit"),
    path('debit', views.debit, name="debit"),
    path('tjcredit', views.tjcredit, name="tjcredit"),
    path('tjdebit', views.tjdebit, name="tjdebit"),
    path('report', views.report, name="report"),
    path('report1', views.report1, name="report1"),

    path('get', views.get, name="get"),
    path('vl', views.vl, name="vl"),
    path('tjl', views.tjl, name="tjl"),
    #path('vp', views.vp, name="vp"),

    # Insert Data in database
    path('post_ve', views.post_ve, name="post_ve"),
    path('post_tj', views.post_tj, name="post_tj"),
    path('post_debit', views.post_debit, name="post_debit"),
    path('post_credit', views.post_credit, name="post_credit"),
    path('tj_post_credit', views.tj_post_credit, name="tj_post_credit"),
    path('tj_post_debit', views.tj_post_debit, name="tj_post_debit"),

    # Login
    path('tjlogin', views.tjlogin, name="tjlogin"),
    path('voucherslogin', views.voucherslogin, name="voucherslogin"),
    path('ledgerlogin', views.ledgerlogin, name="ledgerlogin"),
    path('tjledgerlogin', views.tjledgerlogin, name="tjledgerlogin"),
    path('creditlogin', views.creditlogin, name="creditlogin"),
    path('debitlogin', views.debitlogin, name="debitlogin"),
    path('tjcreditlogin', views.tjcreditlogin, name="tjcreditlogin"),
    path('tjdebitlogin', views.tjdebitlogin, name="tjdebitlogin"),
    path('reportlogin', views.reportlogin, name="reportlogin"),

]
