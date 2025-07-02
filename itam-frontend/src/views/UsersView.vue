<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Users</h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Manage system users and their asset assignments
        </p>
      </v-col>
    </v-row>

    <!-- Users Table -->
    <v-card>
      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="users"
        :loading="loading"
        class="elevation-1"
      >
        <template #item.user="{ item }">
          <div class="d-flex align-center">
            <v-avatar class="mr-3">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
            <div>
              <div class="font-weight-medium">{{ item.full_name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.username }}</div>
            </div>
          </div>
        </template>

        <template #item.email="{ item }">
          <a :href="`mailto:${item.email}`" class="text-decoration-none">
            {{ item.email }}
          </a>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userService, type User } from '@/services/api'

const users = ref<User[]>([])
const loading = ref(false)
const itemsPerPage = ref(10)

const headers = [
  { title: 'User', key: 'user', sortable: false },
  { title: 'Email', key: 'email', sortable: true },
  { title: 'First Name', key: 'first_name', sortable: true },
  { title: 'Last Name', key: 'last_name', sortable: true },
]

onMounted(async () => {
  await loadUsers()
})

async function loadUsers() {
  loading.value = true
  try {
    const response = await userService.getAll()
    users.value = response.data
  } catch (error) {
    console.error('Error loading users:', error)
  } finally {
    loading.value = false
  }
}
</script>

