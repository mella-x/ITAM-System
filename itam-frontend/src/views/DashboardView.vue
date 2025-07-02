<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Dashboard</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Overview of your IT assets and system status
        </p>
      </v-col>
    </v-row>

    <!-- Alerts -->
    <v-row v-if="alerts.length > 0" class="mb-4">
      <v-col>
        <v-alert
          v-for="alert in alerts"
          :key="alert.title"
          :type="alert.type"
          :title="alert.title"
          :text="alert.message"
          class="mb-2"
          closable
        />
      </v-col>
    </v-row>

    <!-- Statistics Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-4" color="primary" dark>
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-desktop-classic</v-icon>
            <div>
              <div class="text-h4 font-weight-bold">{{ stats.total_assets }}</div>
              <div class="text-subtitle-2">Total Assets</div>
            </div>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-4" color="success" dark>
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-check-circle</v-icon>
            <div>
              <div class="text-h4 font-weight-bold">{{ stats.available_assets }}</div>
              <div class="text-subtitle-2">Available</div>
            </div>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-4" color="info" dark>
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-account-check</v-icon>
            <div>
              <div class="text-h4 font-weight-bold">{{ stats.assigned_assets }}</div>
              <div class="text-subtitle-2">Assigned</div>
            </div>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="pa-4" color="warning" dark>
          <div class="d-flex align-center">
            <v-icon size="40" class="mr-4">mdi-wrench</v-icon>
            <div>
              <div class="text-h4 font-weight-bold">{{ stats.maintenance_assets }}</div>
              <div class="text-subtitle-2">Maintenance</div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Additional Stats -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="text-h6">System Overview</v-card-title>
          <v-list>
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-currency-usd</v-icon>
              </template>
              <v-list-item-title>Total Asset Value</v-list-item-title>
              <v-list-item-subtitle>${{ formatCurrency(stats.total_value) }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-shape</v-icon>
              </template>
              <v-list-item-title>Categories</v-list-item-title>
              <v-list-item-subtitle>{{ stats.categories_count }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-map-marker</v-icon>
              </template>
              <v-list-item-title>Locations</v-list-item-title>
              <v-list-item-subtitle>{{ stats.locations_count }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <template #prepend>
                <v-icon>mdi-truck</v-icon>
              </template>
              <v-list-item-title>Vendors</v-list-item-title>
              <v-list-item-subtitle>{{ stats.vendors_count }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card class="pa-4">
          <v-card-title class="text-h6">Asset Status Distribution</v-card-title>
          <div class="mt-4">
            <div class="d-flex justify-space-between align-center mb-2">
              <span>Available</span>
              <span>{{ stats.available_assets }}</span>
            </div>
            <v-progress-linear
              :model-value="(stats.available_assets / stats.total_assets) * 100"
              color="success"
              height="8"
              rounded
              class="mb-3"
            />
            
            <div class="d-flex justify-space-between align-center mb-2">
              <span>Assigned</span>
              <span>{{ stats.assigned_assets }}</span>
            </div>
            <v-progress-linear
              :model-value="(stats.assigned_assets / stats.total_assets) * 100"
              color="info"
              height="8"
              rounded
              class="mb-3"
            />
            
            <div class="d-flex justify-space-between align-center mb-2">
              <span>Maintenance</span>
              <span>{{ stats.maintenance_assets }}</span>
            </div>
            <v-progress-linear
              :model-value="(stats.maintenance_assets / stats.total_assets) * 100"
              color="warning"
              height="8"
              rounded
            />
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Activity -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h6">Recent Assignments</v-card-title>
          <v-card-text>
            <v-list v-if="stats.recent_assignments.length > 0">
              <v-list-item
                v-for="assignment in stats.recent_assignments"
                :key="assignment.id"
                class="px-0"
              >
                <template #prepend>
                  <v-avatar color="primary" size="40">
                    <v-icon>mdi-desktop-classic</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ assignment.asset_name }}</v-list-item-title>
                <v-list-item-subtitle>
                  Assigned to {{ assignment.assigned_to_name }}
                  <br>
                  <small>{{ formatDate(assignment.assigned_date) }}</small>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <div v-else class="text-center py-4 text-medium-emphasis">
              No recent assignments
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h6">Upcoming Maintenance</v-card-title>
          <v-card-text>
            <v-list v-if="stats.upcoming_maintenance.length > 0">
              <v-list-item
                v-for="maintenance in stats.upcoming_maintenance"
                :key="maintenance.id"
                class="px-0"
              >
                <template #prepend>
                  <v-avatar color="warning" size="40">
                    <v-icon>mdi-wrench</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ maintenance.title }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ maintenance.asset_name }}
                  <br>
                  <small>{{ formatDate(maintenance.scheduled_date) }}</small>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
            <div v-else class="text-center py-4 text-medium-emphasis">
              No upcoming maintenance
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { dashboardService, type DashboardStats, type Alert } from '@/services/api'

const stats = ref<DashboardStats>({
  total_assets: 0,
  available_assets: 0,
  assigned_assets: 0,
  maintenance_assets: 0,
  total_value: '0',
  categories_count: 0,
  locations_count: 0,
  vendors_count: 0,
  recent_assignments: [],
  upcoming_maintenance: [],
})

const alerts = ref<Alert[]>([])
const loading = ref(false)

onMounted(async () => {
  await loadDashboardData()
})

async function loadDashboardData() {
  loading.value = true
  try {
    const [statsResponse, alertsResponse] = await Promise.all([
      dashboardService.getStats(),
      dashboardService.getAlerts(),
    ])
    
    stats.value = statsResponse.data
    alerts.value = alertsResponse.data.alerts
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    loading.value = false
  }
}

function formatCurrency(value: string | number): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num)
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
</script>

