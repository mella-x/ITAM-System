<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
      :permanent="$vuetify.display.lgAndUp"
      :temporary="$vuetify.display.mdAndDown"
      width="280"
    >
      <v-list nav>
        <v-list-item
          prepend-icon="mdi-view-dashboard"
          title="Dashboard"
          to="/"
          exact
        />
        <v-list-item
          prepend-icon="mdi-desktop-classic"
          title="Assets"
          to="/assets"
        />
        <v-list-item
          prepend-icon="mdi-account-multiple"
          title="Assignments"
          to="/assignments"
        />
        <v-list-item
          prepend-icon="mdi-wrench"
          title="Maintenance"
          to="/maintenance"
        />
        
        <v-divider class="my-2" />
        
        <v-list-subheader>MANAGEMENT</v-list-subheader>
        <v-list-item
          prepend-icon="mdi-shape"
          title="Categories"
          to="/categories"
        />
        <v-list-item
          prepend-icon="mdi-map-marker"
          title="Locations"
          to="/locations"
        />
        <v-list-item
          prepend-icon="mdi-truck"
          title="Vendors"
          to="/vendors"
        />
        <v-list-item
          prepend-icon="mdi-account-group"
          title="Users"
          to="/users"
        />
        
        <v-divider class="my-2" />
        
        <v-list-item
          prepend-icon="mdi-chart-line"
          title="Reports"
          to="/reports"
        />
        <v-list-item
          prepend-icon="mdi-history"
          title="History"
          to="/history"
        />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left color="primary" dark>
      <v-app-bar-nav-icon
        v-if="$vuetify.display.mdAndDown"
        @click="drawer = !drawer"
      />
      
      <v-toolbar-title class="text-h6">
        <v-icon class="mr-2">mdi-desktop-classic</v-icon>
        ITAM System
      </v-toolbar-title>

      <v-spacer />

      <v-btn icon>
        <v-icon>mdi-bell</v-icon>
      </v-btn>

      <v-menu>
        <template #activator="{ props }">
          <v-btn icon v-bind="props">
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
          <v-list-item>
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item>
          <v-divider />
          <v-list-item @click="logout">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <RouterView />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const drawer = ref(false)
const authStore = useAuthStore()

function logout() {
  authStore.logout()
  // Redirect to login page
  window.location.href = '/login'
}
</script>

<style scoped>
.v-navigation-drawer {
  border-right: 1px solid rgba(0, 0, 0, 0.12);
}
</style>

