<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Asset Assignments</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Track asset assignments and check-in/check-out history
        </p>
      </v-col>
    </v-row>

    <!-- Assignments Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="assignments"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.assigned_date="{ item }">
          {{ formatDate(item.assigned_date) }}
        </template>

        <template #item.return_date="{ item }">
          <span v-if="item.return_date">
            {{ formatDate(item.return_date) }}
          </span>
          <v-chip v-else color="success" size="small">Active</v-chip>
        </template>

        <template #item.is_active="{ item }">
          <v-chip
            :color="item.is_active ? 'success' : 'grey'"
            size="small"
            variant="flat"
          >
            {{ item.is_active ? 'Active' : 'Returned' }}
          </v-chip>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { assignmentService, type AssetAssignment } from '@/services/api'

const assignments = ref<AssetAssignment[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'Asset Tag', key: 'asset_tag', sortable: true },
  { title: 'Asset Name', key: 'asset_name', sortable: true },
  { title: 'Assigned To', key: 'assigned_to_name', sortable: true },
  { title: 'Assigned By', key: 'assigned_by_name', sortable: true },
  { title: 'Assigned Date', key: 'assigned_date', sortable: true },
  { title: 'Return Date', key: 'return_date', sortable: true },
  { title: 'Status', key: 'is_active', sortable: true },
]

onMounted(async () => {
  await loadAssignments()
})

async function loadAssignments() {
  loading.value = true
  try {
    const response = await assignmentService.getAll()
    assignments.value = response.data
  } catch (error) {
    console.error('Error loading assignments:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}
</script>

