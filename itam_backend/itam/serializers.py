from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Asset, AssetCategory, Location, Vendor, AssetAssignment, MaintenanceRecord


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']


class AssetCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = AssetCategory
        fields = '__all__'

    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return AssetCategorySerializer(children, many=True).data


class LocationSerializer(serializers.ModelSerializer):
    asset_count = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    asset_count = serializers.ReadOnlyField()

    class Meta:
        model = Vendor
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField()
    location_name = serializers.ReadOnlyField()
    assigned_to_name = serializers.ReadOnlyField()
    vendor_name = serializers.ReadOnlyField()
    is_assigned = serializers.ReadOnlyField()

    class Meta:
        model = Asset
        fields = '__all__'


class AssetAssignmentSerializer(serializers.ModelSerializer):
    asset_name = serializers.ReadOnlyField()
    asset_tag = serializers.ReadOnlyField()
    assigned_to_name = serializers.ReadOnlyField()
    assigned_by_name = serializers.ReadOnlyField()

    class Meta:
        model = AssetAssignment
        fields = '__all__'


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    asset_name = serializers.ReadOnlyField()
    asset_tag = serializers.ReadOnlyField()
    vendor_name = serializers.ReadOnlyField()
    created_by_name = serializers.ReadOnlyField()

    class Meta:
        model = MaintenanceRecord
        fields = '__all__'

