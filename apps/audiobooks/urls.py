from django.urls import path
from .views import dashboard_view, detalle_view
urlpatterns = [
    path('', dashboard_view, name="dashboard"),
    path('detalle/<int:id>', detalle_view, name="detalle"),
]