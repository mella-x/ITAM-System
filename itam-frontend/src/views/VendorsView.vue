<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Vendors</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage vendors and suppliers for asset procurement and maintenance
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus">
          Add Vendor
        </v-btn>
      </v-col>
    </v-row>

    <!-- Vendors Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="vendors"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.name="{ item }">
          <div>
            <div class="font-weight-medium">{{ item.name }}</div>
            <div v-if="item.website" class="text-caption">
              <a :href="item.website" target="_blank" class="text-decoration-none">
                {{ item.website }}
              </a>
            </div>
          </div>
        </template>

        <template #item.contact="{ item }">
          <div v-if="item.contact_person || item.email || item.phone">
            <div v-if="item.contact_person" class="font-weight-medium">
              {{ item.contact_person }}
            </div>
            <div v-if="item.email" class="text-caption">
              {{ item.email }}
            </div>
            <div v-if="item.phone" class="text-caption">
              {{ item.phone }}
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
import { vendorService, type Vendor } from '@/services/api'

const vendors = ref<Vendor[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Contact Information', key: 'contact', sortable: false },
  { title: 'Assets', key: 'asset_count', sortable: true },
  { title: 'Status', key: 'is_active', sortable: true },
  { title: 'Created', key: 'created_at', sortable: true },
]

onMounted(async () => {
  await loadVendors()
})

async function loadVendors() {
  loading.value = true
  try {
    const response = await vendorService.getAll()
    vendors.value = response.data
  } catch (error) {
    console.error('Error loading vendors:', error)
  } finally {
    loading.value = false
  }
}
</script>

