from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import MenuItemViewSet, OrderViewSet, average_daily_sales
from django.contrib import admin
from django.urls import path, include

router = DefaultRouter()
router.register('menu-items', MenuItemViewSet, basename='menuitem')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('analytics/average-daily-sales/', average_daily_sales),
]
