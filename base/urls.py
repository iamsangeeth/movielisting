from django.urls import path
from base.views import *

urlpatterns = [
    path('register/', Register.as_view(), name='login_token'),
    path('movies/', MoviesList.as_view(), name='movies_list'),
    path('collection/', CollectionsView.as_view(), name='collections'),
    path('collection/<str:pk>/', CollectionDetails.as_view(), name='collections'),
    path('request-count/', RequestView.as_view(), name='request_count'),
    path('request-count/reset/', RequestResetView.as_view(), name='request_count_reset'),
]