import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/assets',
      name: 'assets',
      component: () => import('../views/AssetsView.vue'),
    },
    {
      path: '/assignments',
      name: 'assignments',
      component: () => import('../views/AssignmentsView.vue'),
    },
    {
      path: '/maintenance',
      name: 'maintenance',
      component: () => import('../views/MaintenanceView.vue'),
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/CategoriesView.vue'),
    },
    {
      path: '/locations',
      name: 'locations',
      component: () => import('../views/LocationsView.vue'),
    },
    {
      path: '/vendors',
      name: 'vendors',
      component: () => import('../views/VendorsView.vue'),
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('../views/UsersView.vue'),
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('../views/ReportsView.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue'),
    },
  ],
})

export default router
