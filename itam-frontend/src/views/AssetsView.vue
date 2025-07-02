<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Assets</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage your IT assets and equipment
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn
          color="primary"
          prepend-icon="mdi-plus"
          @click="showCreateDialog = true"
        >
          Add Asset
        </v-btn>
      </v-col>
    </v-row>

    <!-- Filters -->
    <v-card class="mb-4">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="search"
              label="Search assets..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="compact"
              clearable
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="statusFilter"
              :items="statusOptions"
              label="Status"
              variant="outlined"
              density="compact"
              clearable
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="categoryFilter"
              :items="categories"
              item-title="name"
              item-value="id"
              label="Category"
              variant="outlined"
              density="compact"
              clearable
            />
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="locationFilter"
              :items="locations"
              item-title="name"
              item-value="id"
              label="Location"
              variant="outlined"
              density="compact"
              clearable
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Assets Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="filteredAssets"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
            variant="flat"
          >
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>

        <template #item.condition="{ item }">
          <v-chip
            :color="getConditionColor(item.condition)"
            size="small"
            variant="outlined"
          >
            {{ getConditionText(item.condition) }}
          </v-chip>
        </template>

        <template #item.purchase_cost="{ item }">
          <span v-if="item.purchase_cost">
            ${{ formatCurrency(item.purchase_cost) }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <template #item.current_value="{ item }">
          <span v-if="item.current_value">
            ${{ formatCurrency(item.current_value) }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <template #item.assigned_to_name="{ item }">
          <div v-if="item.assigned_to_name" class="d-flex align-center">
            <v-avatar size="24" class="mr-2">
              <v-icon size="16">mdi-account</v-icon>
            </v-avatar>
            {{ item.assigned_to_name }}
          </div>
          <span v-else class="text-medium-emphasis">Unassigned</span>
        </template>

        <template #item.actions="{ item }">
          <v-btn
            icon="mdi-eye"
            size="small"
            variant="text"
            @click="viewAsset(item)"
          />
          <v-btn
            icon="mdi-pencil"
            size="small"
            variant="text"
            @click="editAsset(item)"
          />
          <v-btn
            v-if="!item.assigned_to"
            icon="mdi-account-plus"
            size="small"
            variant="text"
            color="primary"
            @click="assignAsset(item)"
          />
          <v-btn
            v-else
            icon="mdi-account-minus"
            size="small"
            variant="text"
            color="warning"
            @click="unassignAsset(item)"
          />
          <v-btn
            icon="mdi-delete"
            size="small"
            variant="text"
            color="error"
            @click="deleteAsset(item)"
          />
        </template>
      </v-data-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <AssetDialog
      v-model="showCreateDialog"
      :asset="selectedAsset"
      :categories="categories"
      :locations="locations"
      :vendors="vendors"
      @saved="onAssetSaved"
    />

    <!-- Assign Dialog -->
    <AssignDialog
      v-model="showAssignDialog"
      :asset="selectedAsset"
      :users="users"
      @assigned="onAssetAssigned"
    />

    <!-- View Dialog -->
    <AssetViewDialog
      v-model="showViewDialog"
      :asset="selectedAsset"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  assetService, 
  categoryService, 
  locationService, 
  vendorService,
  userService,
  type Asset, 
  type AssetCategory, 
  type Location, 
  type Vendor,
  type User
} from '@/services/api'
import AssetDialog from '@/components/AssetDialog.vue'
import AssignDialog from '@/components/AssignDialog.vue'
import AssetViewDialog from '@/components/AssetViewDialog.vue'

const assets = ref<Asset[]>([])
const categories = ref<AssetCategory[]>([])
const locations = ref<Location[]>([])
const vendors = ref<Vendor[]>([])
const users = ref<User[]>([])
const loading = ref(false)
const search = ref('')
const statusFilter = ref('')
const categoryFilter = ref('')
const locationFilter = ref('')
const itemsPerPage = ref(10)

const showCreateDialog = ref(false)
const showAssignDialog = ref(false)
const showViewDialog = ref(false)
const selectedAsset = ref<Asset | null>(null)

const statusOptions = [
  { title: 'Available', value: 'available' },
  { title: 'Assigned', value: 'assigned' },
  { title: 'In Use', value: 'in_use' },
  { title: 'Maintenance', value: 'maintenance' },
  { title: 'Repair', value: 'repair' },
  { title: 'Retired', value: 'retired' },
  { title: 'Disposed', value: 'disposed' },
  { title: 'Lost', value: 'lost' },
  { title: 'Stolen', value: 'stolen' },
]

const headers = [
  { title: 'Asset Tag', key: 'asset_tag', sortable: true },
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Category', key: 'category_name', sortable: true },
  { title: 'Brand', key: 'brand', sortable: true },
  { title: 'Model', key: 'model', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Condition', key: 'condition', sortable: true },
  { title: 'Location', key: 'location_name', sortable: true },
  { title: 'Assigned To', key: 'assigned_to_name', sortable: true },
  { title: 'Purchase Cost', key: 'purchase_cost', sortable: true },
  { title: 'Current Value', key: 'current_value', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false },
]

const filteredAssets = computed(() => {
  let filtered = assets.value

  if (statusFilter.value) {
    filtered = filtered.filter(asset => asset.status === statusFilter.value)
  }

  if (categoryFilter.value) {
    filtered = filtered.filter(asset => asset.category === categoryFilter.value)
  }

  if (locationFilter.value) {
    filtered = filtered.filter(asset => asset.location === locationFilter.value)
  }

  return filtered
})

onMounted(async () => {
  await loadData()
})

async function loadData() {
  loading.value = true
  try {
    const [assetsRes, categoriesRes, locationsRes, vendorsRes, usersRes] = await Promise.all([
      assetService.getAll(),
      categoryService.getAll(),
      locationService.getAll(),
      vendorService.getAll(),
      userService.getAll(),
    ])

    assets.value = assetsRes.data
    categories.value = categoriesRes.data
    locations.value = locationsRes.data
    vendors.value = vendorsRes.data
    users.value = usersRes.data
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

function viewAsset(asset: Asset) {
  selectedAsset.value = asset
  showViewDialog.value = true
}

function editAsset(asset: Asset) {
  selectedAsset.value = asset
  showCreateDialog.value = true
}

function assignAsset(asset: Asset) {
  selectedAsset.value = asset
  showAssignDialog.value = true
}

async function unassignAsset(asset: Asset) {
  try {
    await assetService.unassign(asset.id, { notes: 'Unassigned from dashboard' })
    await loadData()
  } catch (error) {
    console.error('Error unassigning asset:', error)
  }
}

async function deleteAsset(asset: Asset) {
  if (confirm(`Are you sure you want to delete asset ${asset.asset_tag}?`)) {
    try {
      await assetService.delete(asset.id)
      await loadData()
    } catch (error) {
      console.error('Error deleting asset:', error)
    }
  }
}

function onAssetSaved() {
  showCreateDialog.value = false
  selectedAsset.value = null
  loadData()
}

function onAssetAssigned() {
  showAssignDialog.value = false
  selectedAsset.value = null
  loadData()
}

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    available: 'success',
    assigned: 'info',
    in_use: 'primary',
    maintenance: 'warning',
    repair: 'orange',
    retired: 'grey',
    disposed: 'grey-darken-2',
    lost: 'error',
    stolen: 'red-darken-2',
  }
  return colors[status] || 'grey'
}

function getStatusText(status: string): string {
  return statusOptions.find(option => option.value === status)?.title || status
}

function getConditionColor(condition: string): string {
  const colors: Record<string, string> = {
    excellent: 'success',
    good: 'info',
    fair: 'warning',
    poor: 'orange',
    broken: 'error',
  }
  return colors[condition] || 'grey'
}

function getConditionText(condition: string): string {
  return condition.charAt(0).toUpperCase() + condition.slice(1)
}

function formatCurrency(value: string | number): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num)
}
</script>

