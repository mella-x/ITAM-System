<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Locations</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage physical locations where assets are stored or used
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus">
          Add Location
        </v-btn>
      </v-col>
    </v-row>

    <!-- Locations Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="locations"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.name="{ item }">
          <div>
            <div class="font-weight-medium">{{ item.name }}</div>
            <div v-if="item.address" class="text-caption text-medium-emphasis">
              {{ item.address }}
            </div>
          </div>
        </template>

        <template #item.location="{ item }">
          <div v-if="item.city || item.state || item.country">
            {{ [item.city, item.state, item.country].filter(Boolean).join(', ') }}
          </div>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <template #item.contact="{ item }">
          <div v-if="item.contact_person || item.contact_email">
            <div v-if="item.contact_person" class="font-weight-medium">
              {{ item.contact_person }}
            </div>
            <div v-if="item.contact_email" class="text-caption">
              {{ item.contact_email }}
            </div>
          </div>
          <span v-else class="text-medium-emphasis">-</span>
        </template>

        <template #item.asset_count="{ item }">
          <v-chip
            :color="item.asset_count > 0 ? 'primary' : 'grey'"
            size="small"
            variant="outlined"
          >
            {{ item.asset_count }} assets
          </v-chip>
        </template>

        <template #item.is_active="{ item }">
          <v-chip
            :color="item.is_active ? 'success' : 'grey'"
            size="small"
            variant="flat"
          >
            {{ item.is_active ? 'Active' : 'Inactive' }}
          </v-chip>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { locationService, type Location } from '@/services/api'

const locations = ref<Location[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Location', key: 'location', sortable: false },
  { title: 'Contact', key: 'contact', sortable: false },
  { title: 'Assets', key: 'asset_count', sortable: true },
  { title: 'Status', key: 'is_active', sortable: true },
  { title: 'Created', key: 'created_at', sortable: true },
]

onMounted(async () => {
  await loadLocations()
})

async function loadLocations() {
  loading.value = true
  try {
    const response = await locationService.getAll()
    locations.value = response.data
  } catch (error) {
    console.error('Error loading locations:', error)
  } finally {
    loading.value = false
  }
}
</script>

