from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssetViewSet, AssetCategoryViewSet, LocationViewSet, 
    VendorViewSet, UserViewSet, AssetAssignmentViewSet, 
    MaintenanceRecordViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'categories', AssetCategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'users', UserViewSet)
router.register(r'assignments', AssetAssignmentViewSet)
router.register(r'maintenance', MaintenanceRecordViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('api/', include(router.urls)),
]

