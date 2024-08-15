from django.contrib import admin
from django.urls import path

from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ItemsListView.as_view(), name="items"),
    path('item/<int:pk>/', ItemPageView.as_view(), name="item"),
    path('buy/<int:pk>/', CreateCheckoutSessionView.as_view(), name="buy"),
    path('success/', SuccessView.as_view(), name="success"),
    path('cancel/', CancelView.as_view(), name="cancel"),
]
