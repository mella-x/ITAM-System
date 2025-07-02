<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Asset Categories</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Organize your assets with categories and subcategories
        </p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" prepend-icon="mdi-plus">
          Add Category
        </v-btn>
      </v-col>
    </v-row>

    <!-- Categories Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="categories"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.name="{ item }">
          <div class="d-flex align-center">
            <v-icon v-if="item.icon" class="mr-2">{{ item.icon }}</v-icon>
            <span>{{ item.name }}</span>
          </div>
        </template>

        <template #item.parent="{ item }">
          <span v-if="item.parent">
            {{ getParentName(item.parent) }}
          </span>
          <span v-else class="text-medium-emphasis">Root Category</span>
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

        <template #item.children="{ item }">
          <v-chip
            v-if="item.children.length > 0"
            color="info"
            size="small"
            variant="outlined"
          >
            {{ item.children.length }} subcategories
          </v-chip>
          <span v-else class="text-medium-emphasis">-</span>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { categoryService, type AssetCategory } from '@/services/api'

const categories = ref<AssetCategory[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Description', key: 'description', sortable: true },
  { title: 'Parent Category', key: 'parent', sortable: true },
  { title: 'Status', key: 'is_active', sortable: true },
  { title: 'Subcategories', key: 'children', sortable: false },
  { title: 'Created', key: 'created_at', sortable: true },
]

onMounted(async () => {
  await loadCategories()
})

async function loadCategories() {
  loading.value = true
  try {
    const response = await categoryService.getAll()
    categories.value = response.data
  } catch (error) {
    console.error('Error loading categories:', error)
  } finally {
    loading.value = false
  }
}

function getParentName(parentId: number): string {
  const parent = categories.value.find(cat => cat.id === parentId)
  return parent?.name || 'Unknown'
}
</script>

