from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Asset, AssetCategory, Location, Vendor, AssetAssignment, MaintenanceRecord
from .serializers import (
    AssetSerializer, AssetCategorySerializer, LocationSerializer, 
    VendorSerializer, UserSerializer, AssetAssignmentSerializer, 
    MaintenanceRecordSerializer
)


class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.filter(is_active=True)
    serializer_class = AssetCategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter(is_active=True)
    serializer_class = VendorSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        asset = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        notes = request.data.get('notes', '')

        if not assigned_to_id:
            return Response({'error': 'assigned_to is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update asset
        asset.assigned_to = assigned_to
        asset.status = 'assigned'
        asset.save()

        # Create assignment record
        AssetAssignment.objects.create(
            asset=asset,
            assigned_to=assigned_to,
            assigned_by=request.user if request.user.is_authenticated else User.objects.first(),
            notes=notes
        )

        return Response({'message': 'Asset assigned successfully'})

    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        asset = self.get_object()
        notes = request.data.get('notes', '')

        if asset.assigned_to:
            # Update assignment record
            assignment = AssetAssignment.objects.filter(
                asset=asset, 
                is_active=True
            ).first()
            if assignment:
                assignment.is_active = False
                assignment.notes += f"\nReturned: {notes}" if notes else ""
                assignment.save()

            # Update asset
            asset.assigned_to = None
            asset.status = 'available'
            asset.save()

        return Response({'message': 'Asset unassigned successfully'})

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        asset = self.get_object()
        assignments = AssetAssignment.objects.filter(asset=asset).order_by('-assigned_date')
        maintenance = MaintenanceRecord.objects.filter(asset=asset).order_by('-created_at')
        
        return Response({
            'assignments': AssetAssignmentSerializer(assignments, many=True).data,
            'maintenance': MaintenanceRecordSerializer(maintenance, many=True).data
        })


class AssetAssignmentViewSet(viewsets.ModelViewSet):
    queryset = AssetAssignment.objects.all()
    serializer_class = AssetAssignmentSerializer


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer


class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_assets = Asset.objects.count()
        available_assets = Asset.objects.filter(status='available').count()
        assigned_assets = Asset.objects.filter(status='assigned').count()
        maintenance_assets = Asset.objects.filter(status='maintenance').count()
        
        total_value = Asset.objects.aggregate(
            total=Sum('purchase_cost')
        )['total'] or 0

        categories_count = AssetCategory.objects.filter(is_active=True).count()
        locations_count = Location.objects.filter(is_active=True).count()
        vendors_count = Vendor.objects.filter(is_active=True).count()

        recent_assignments = AssetAssignment.objects.filter(
            is_active=True
        ).order_by('-assigned_date')[:5]

        upcoming_maintenance = MaintenanceRecord.objects.filter(
            status='scheduled'
        ).order_by('scheduled_date')[:5]

        return Response({
            'total_assets': total_assets,
            'available_assets': available_assets,
            'assigned_assets': assigned_assets,
            'maintenance_assets': maintenance_assets,
            'total_value': str(total_value),
            'categories_count': categories_count,
            'locations_count': locations_count,
            'vendors_count': vendors_count,
            'recent_assignments': AssetAssignmentSerializer(recent_assignments, many=True).data,
            'upcoming_maintenance': MaintenanceRecordSerializer(upcoming_maintenance, many=True).data,
        })

    @action(detail=False, methods=['get'])
    def alerts(self, request):
        alerts = []
        
        # Check for assets without maintenance
        assets_needing_maintenance = Asset.objects.filter(
            status__in=['in_use', 'assigned'],
            maintenance_records__isnull=True
        ).count()
        
        if assets_needing_maintenance > 0:
            alerts.append({
                'type': 'warning',
                'title': 'Maintenance Required',
                'message': f'{assets_needing_maintenance} assets may need maintenance scheduling',
                'count': assets_needing_maintenance
            })

        # Check for overdue maintenance
        overdue_maintenance = MaintenanceRecord.objects.filter(
            status='scheduled',
            scheduled_date__lt=timezone.now()
        ).count()
        
        if overdue_maintenance > 0:
            alerts.append({
                'type': 'error',
                'title': 'Overdue Maintenance',
                'message': f'{overdue_maintenance} maintenance tasks are overdue',
                'count': overdue_maintenance
            })

        return Response({'alerts': alerts})

