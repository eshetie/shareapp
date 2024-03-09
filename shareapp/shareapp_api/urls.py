from django.shortcuts import render

# Create your views here.
from django.urls import path, include
from .views import UsersListApiView,UsersDetailApiView,UsersLoginView,AllCompanyListView,purchaseDetail,ShareDetailView,SaveBillFromCartView,AllsharesunderCompany,GetBillHistoryView,GetOutstandingDetails,GetCompletedDetails,SearchCompanyListView

urlpatterns = [
    path('api', UsersListApiView.as_view()),
    path('api/login/', UsersLoginView.as_view()),
    path('api/get/user/<phone>/', UsersDetailApiView.as_view()),
    path('api/get/purchased/<phone>/', purchaseDetail.as_view()),
    path('api/get/company/<name>/', SearchCompanyListView.as_view()),
    path('api/get/companys/', AllCompanyListView.as_view()),
    path('api/addtoCart/', purchaseDetail.as_view()),
    path('api/get/shares/<companyname>/', AllsharesunderCompany.as_view()),
    path('api/addShare/', ShareDetailView.as_view()),
    path('api/addbill/', SaveBillFromCartView.as_view()),
    path('api/get/bills/<phone>/', GetBillHistoryView.as_view()),
    path('api/get/outstanding/<phone>/', GetOutstandingDetails.as_view()),
    path('api/get/completed/<phone>/', GetCompletedDetails.as_view()),
]