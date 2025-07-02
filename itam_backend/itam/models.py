from django.db import models
from django.contrib.auth.models import User


class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Asset Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def asset_count(self):
        return self.assets.count()


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

    def __str__(self):
        return self.name

    @property
    def asset_count(self):
        return self.assets.count()


class Asset(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
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

    asset_tag = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets')
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='assets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_assets')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    warranty_start_date = models.DateField(null=True, blank=True)
    warranty_end_date = models.DateField(null=True, blank=True)
    warranty_provider = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    qr_code = models.CharField(max_length=100, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"

    @property
    def is_assigned(self):
        return self.assigned_to is not None

    @property
    def category_name(self):
        return self.category.name if self.category else ''

    @property
    def location_name(self):
        return self.location.name if self.location else ''

    @property
    def assigned_to_name(self):
        return self.assigned_to.get_full_name() if self.assigned_to else ''

    @property
    def vendor_name(self):
        return self.vendor.name if self.vendor else ''


class AssetAssignment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='assignments')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_made')
    assigned_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def asset_name(self):
        return self.asset.name

    @property
    def asset_tag(self):
        return self.asset.asset_tag

    @property
    def assigned_to_name(self):
        return self.assigned_to.get_full_name()

    @property
    def assigned_by_name(self):
        return self.assigned_by.get_full_name()


class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
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

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    performed_by = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def asset_name(self):
        return self.asset.name

    @property
    def asset_tag(self):
        return self.asset.asset_tag

    @property
    def vendor_name(self):
        return self.vendor.name if self.vendor else ''

    @property
    def created_by_name(self):
        return self.created_by.get_full_name()

