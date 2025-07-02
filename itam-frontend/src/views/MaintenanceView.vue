<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Maintenance</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Schedule and track asset maintenance activities
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus">
          Schedule Maintenance
        </v-btn>
      </v-col>
    </v-row>

    <!-- Maintenance Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="maintenanceRecords"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.maintenance_type="{ item }">
          <v-chip
            :color="getMaintenanceTypeColor(item.maintenance_type)"
            size="small"
            variant="outlined"
          >
            {{ getMaintenanceTypeText(item.maintenance_type) }}
          </v-chip>
        </template>

        <template #item.status="{ item }">
          <v-chip
            :color="getStatusColor(item.status)"
            size="small"
            variant="flat"
          >
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>

        <template #item.scheduled_date="{ item }">
          {{ formatDate(item.scheduled_date) }}
        </template>

        <template #item.completed_date="{ item }">
          <span v-if="item.completed_date">
            {{ formatDate(item.completed_date) }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <template #item.cost="{ item }">
          <span v-if="item.cost">
            ${{ formatCurrency(item.cost) }}
          </span>
          <span v-else class="text-medium-emphasis">-</span>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { maintenanceService, type MaintenanceRecord } from '@/services/api'

const maintenanceRecords = ref<MaintenanceRecord[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'Asset', key: 'asset_name', sortable: true },
  { title: 'Title', key: 'title', sortable: true },
  { title: 'Type', key: 'maintenance_type', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Scheduled Date', key: 'scheduled_date', sortable: true },
  { title: 'Completed Date', key: 'completed_date', sortable: true },
  { title: 'Cost', key: 'cost', sortable: true },
  { title: 'Vendor', key: 'vendor_name', sortable: true },
]

onMounted(async () => {
  await loadMaintenanceRecords()
})

async function loadMaintenanceRecords() {
  loading.value = true
  try {
    const response = await maintenanceService.getAll()
    maintenanceRecords.value = response.data
  } catch (error) {
    console.error('Error loading maintenance records:', error)
  } finally {
    loading.value = false
  }
}

function getMaintenanceTypeColor(type: string): string {
  const colors: Record<string, string> = {
    preventive: 'success',
    corrective: 'warning',
    emergency: 'error',
    upgrade: 'info',
    inspection: 'primary',
  }
  return colors[type] || 'grey'
}

function getMaintenanceTypeText(type: string): string {
  return type.charAt(0).toUpperCase() + type.slice(1)
}

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    scheduled: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'error',
  }
  return colors[status] || 'grey'
}

function getStatusText(status: string): string {
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function formatCurrency(value: string | number): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num)
}
</script>

