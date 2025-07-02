# ITAM Database Schema Design

## Core Models

### 1. Asset Categories
```python
class AssetCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, blank=True)  # For UI icons
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Asset Categories"
```

### 2. Locations/Departments
```python
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 3. Vendors/Suppliers
```python
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 4. Assets (Core Model)
```python
class Asset(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('repair', 'Under Repair'),
        ('retired', 'Retired'),
        ('disposed', 'Disposed'),
        ('lost', 'Lost'),
        ('stolen', 'Stolen'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('broken', 'Broken'),
    ]
    
    # Basic Information
    asset_tag = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    
    # Asset Details
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    # Status and Condition
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Location and Assignment
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    assigned_to = models.ForeignKey('users.ClientUser', null=True, blank=True, on_delete=models.SET_NULL)
    
    # Purchase Information
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.SET_NULL)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    
    # Warranty Information
    warranty_start_date = models.DateField(null=True, blank=True)
    warranty_end_date = models.DateField(null=True, blank=True)
    warranty_provider = models.CharField(max_length=100, blank=True)
    
    # Depreciation
    depreciation_method = models.CharField(max_length=50, default='straight_line')
    useful_life_years = models.IntegerField(default=3)
    salvage_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional Information
    notes = models.TextField(blank=True)
    custom_fields = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.ClientUser', on_delete=models.PROTECT, related_name='created_assets')
    
    class Meta:
        ordering = ['-created_at']
```

### 5. Asset Assignments
```python
class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('users.ClientUser', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey('users.ClientUser', on_delete=models.PROTECT, related_name='assignments_made')
    assigned_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-assigned_date']
```

### 6. Maintenance Records
```python
class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPES = [
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('emergency', 'Emergency'),
        ('upgrade', 'Upgrade'),
        ('inspection', 'Inspection'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    performed_by = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.ClientUser', on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['-scheduled_date']
```

### 7. Asset History/Audit Trail
```python
class AssetHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('assigned', 'Assigned'),
        ('unassigned', 'Unassigned'),
        ('moved', 'Moved'),
        ('maintenance', 'Maintenance'),
        ('status_changed', 'Status Changed'),
    ]
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.ClientUser', on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Asset Histories"
```

### 8. Software Licenses (for Software Assets)
```python
class SoftwareLicense(models.Model):
    LICENSE_TYPES = [
        ('perpetual', 'Perpetual'),
        ('subscription', 'Subscription'),
        ('volume', 'Volume'),
        ('oem', 'OEM'),
        ('trial', 'Trial'),
    ]
    
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=500, blank=True)
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPES)
    
    total_licenses = models.IntegerField(default=1)
    used_licenses = models.IntegerField(default=0)
    
    expiry_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    
    support_included = models.BooleanField(default=False)
    support_expiry_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## API Endpoints Structure

### Asset Management
- `GET /api/assets/` - List all assets with filtering and pagination
- `POST /api/assets/` - Create new asset
- `GET /api/assets/{id}/` - Get asset details
- `PUT /api/assets/{id}/` - Update asset
- `DELETE /api/assets/{id}/` - Delete asset
- `GET /api/assets/{id}/history/` - Get asset history
- `POST /api/assets/{id}/assign/` - Assign asset to user
- `POST /api/assets/{id}/unassign/` - Unassign asset

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Locations
- `GET /api/locations/` - List locations
- `POST /api/locations/` - Create location
- `GET /api/locations/{id}/` - Get location details
- `PUT /api/locations/{id}/` - Update location
- `DELETE /api/locations/{id}/` - Delete location

### Vendors
- `GET /api/vendors/` - List vendors
- `POST /api/vendors/` - Create vendor
- `GET /api/vendors/{id}/` - Get vendor details
- `PUT /api/vendors/{id}/` - Update vendor
- `DELETE /api/vendors/{id}/` - Delete vendor

### Maintenance
- `GET /api/maintenance/` - List maintenance records
- `POST /api/maintenance/` - Create maintenance record
- `GET /api/maintenance/{id}/` - Get maintenance details
- `PUT /api/maintenance/{id}/` - Update maintenance record
- `DELETE /api/maintenance/{id}/` - Delete maintenance record

### Reports
- `GET /api/reports/assets/` - Asset reports
- `GET /api/reports/maintenance/` - Maintenance reports
- `GET /api/reports/depreciation/` - Depreciation reports
- `GET /api/reports/assignments/` - Assignment reports

### Dashboard
- `GET /api/dashboard/stats/` - Dashboard statistics
- `GET /api/dashboard/alerts/` - System alerts and notifications

