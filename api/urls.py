from django.urls import path, re_path
from .apiview import HomeLandingData, TransactionApi, TransactionDetailApi
urlpatterns = [
    path('home', HomeLandingData.as_view(), name='home-api'),
    path('transaction', TransactionApi.as_view(), name='transaction-api'),
    re_path('transaction-detail/(?P<pk>\d+)/$',
            TransactionDetailApi.as_view(), name='transaction-detail-api')
]
