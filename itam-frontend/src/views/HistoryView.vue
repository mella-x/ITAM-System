<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Asset History</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          View audit trail and history of all asset changes
        </p>
      </v-col>
    </v-row>

    <!-- History Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="history"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.action="{ item }">
          <v-chip
            :color="getActionColor(item.action)"
            size="small"
            variant="outlined"
          >
            {{ getActionText(item.action) }}
          </v-chip>
        </template>

        <template #item.asset="{ item }">
          <div>
            <div class="font-weight-medium">{{ item.asset_name }}</div>
            <div class="text-caption text-medium-emphasis">{{ item.asset_tag }}</div>
          </div>
        </template>

        <template #item.created_at="{ item }">
          {{ formatDateTime(item.created_at) }}
        </template>

        <template #item.created_by_name="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="24" class="mr-2">
              <v-icon size="16">mdi-account</v-icon>
            </v-avatar>
            {{ item.created_by_name }}
          </div>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { assetService } from '@/services/api'

const history = ref<any[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'Asset', key: 'asset', sortable: false },
  { title: 'Action', key: 'action', sortable: true },
  { title: 'Description', key: 'description', sortable: false },
  { title: 'Date', key: 'created_at', sortable: true },
  { title: 'User', key: 'created_by_name', sortable: true },
]

onMounted(async () => {
  await loadHistory()
})

async function loadHistory() {
  loading.value = true
  try {
    // This would need to be implemented in the API service
    // For now, we'll show an empty state
    history.value = []
  } catch (error) {
    console.error('Error loading history:', error)
  } finally {
    loading.value = false
  }
}

function getActionColor(action: string): string {
  const colors: Record<string, string> = {
    created: 'success',
    updated: 'info',
    assigned: 'primary',
    unassigned: 'warning',
    moved: 'purple',
    maintenance: 'orange',
    status_changed: 'blue',
    condition_changed: 'teal',
  }
  return colors[action] || 'grey'
}

function getActionText(action: string): string {
  return action.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

function formatDateTime(dateString: string): string {
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

