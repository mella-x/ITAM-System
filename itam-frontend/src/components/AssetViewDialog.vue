<template>
  <v-dialog v-model="dialog" max-width="900px">
    <v-card v-if="asset">
      <v-card-title class="text-h5 d-flex align-center">
        <v-icon class="mr-2">mdi-desktop-classic</v-icon>
        {{ asset.name }}
        <v-spacer />
        <v-chip
          :color="getStatusColor(asset.status)"
          size="small"
          variant="flat"
        >
          {{ getStatusText(asset.status) }}
        </v-chip>
      </v-card-title>

      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="outlined" class="mb-4">
              <v-card-title class="text-h6">Basic Information</v-card-title>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item>
                    <v-list-item-title>Asset Tag</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.asset_tag }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Name</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.name }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.description">
                    <v-list-item-title>Description</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.description }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Category</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.category_name }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Location</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.location_name }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <v-card variant="outlined" class="mb-4">
              <v-card-title class="text-h6">Asset Details</v-card-title>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item v-if="asset.brand">
                    <v-list-item-title>Brand</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.brand }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.model">
                    <v-list-item-title>Model</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.model }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.serial_number">
                    <v-list-item-title>Serial Number</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.serial_number }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Condition</v-list-item-title>
                    <v-list-item-subtitle>
                      <v-chip
                        :color="getConditionColor(asset.condition)"
                        size="small"
                        variant="outlined"
                      >
                        {{ getConditionText(asset.condition) }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.qr_code">
                    <v-list-item-title>QR Code / Barcode</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.qr_code }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card variant="outlined" class="mb-4">
              <v-card-title class="text-h6">Assignment</v-card-title>
              <v-card-text>
                <div v-if="asset.assigned_to_name" class="d-flex align-center">
                  <v-avatar class="mr-3">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                  <div>
                    <div class="font-weight-medium">{{ asset.assigned_to_name }}</div>
                    <div class="text-caption text-medium-emphasis">Assigned User</div>
                  </div>
                </div>
                <div v-else class="text-center py-4 text-medium-emphasis">
                  <v-icon size="48" class="mb-2">mdi-account-off</v-icon>
                  <div>Not assigned to any user</div>
                </div>
              </v-card-text>
            </v-card>

            <v-card variant="outlined" class="mb-4">
              <v-card-title class="text-h6">Financial Information</v-card-title>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item v-if="asset.purchase_date">
                    <v-list-item-title>Purchase Date</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDate(asset.purchase_date) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.purchase_cost">
                    <v-list-item-title>Purchase Cost</v-list-item-title>
                    <v-list-item-subtitle>${{ formatCurrency(asset.purchase_cost) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.current_value">
                    <v-list-item-title>Current Value</v-list-item-title>
                    <v-list-item-subtitle>${{ formatCurrency(asset.current_value) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.vendor_name">
                    <v-list-item-title>Vendor</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.vendor_name }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.invoice_number">
                    <v-list-item-title>Invoice Number</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.invoice_number }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <v-card variant="outlined" class="mb-4" v-if="asset.warranty_start_date || asset.warranty_end_date">
              <v-card-title class="text-h6">Warranty Information</v-card-title>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item v-if="asset.warranty_start_date">
                    <v-list-item-title>Warranty Start</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDate(asset.warranty_start_date) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.warranty_end_date">
                    <v-list-item-title>Warranty End</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDate(asset.warranty_end_date) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item v-if="asset.warranty_provider">
                    <v-list-item-title>Warranty Provider</v-list-item-title>
                    <v-list-item-subtitle>{{ asset.warranty_provider }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row v-if="asset.notes">
          <v-col cols="12">
            <v-card variant="outlined">
              <v-card-title class="text-h6">Notes</v-card-title>
              <v-card-text>
                <p>{{ asset.notes }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-card variant="outlined">
              <v-card-title class="text-h6">System Information</v-card-title>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item>
                    <v-list-item-title>Created</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDateTime(asset.created_at) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Last Updated</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDateTime(asset.updated_at) }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          @click="dialog = false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Asset } from '@/services/api'

interface Props {
  modelValue: boolean
  asset?: Asset | null
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    available: 'success',
    assigned: 'info',
    in_use: 'primary',
    maintenance: 'warning',
    repair: 'orange',
    retired: 'grey',
    disposed: 'grey-darken-2',
    lost: 'error',
    stolen: 'red-darken-2',
  }
  return colors[status] || 'grey'
}

function getStatusText(status: string): string {
  const statusOptions = [
    { title: 'Available', value: 'available' },
    { title: 'Assigned', value: 'assigned' },
    { title: 'In Use', value: 'in_use' },
    { title: 'Maintenance', value: 'maintenance' },
    { title: 'Repair', value: 'repair' },
    { title: 'Retired', value: 'retired' },
    { title: 'Disposed', value: 'disposed' },
    { title: 'Lost', value: 'lost' },
    { title: 'Stolen', value: 'stolen' },
  ]
  return statusOptions.find(option => option.value === status)?.title || status
}

function getConditionColor(condition: string): string {
  const colors: Record<string, string> = {
    excellent: 'success',
    good: 'info',
    fair: 'warning',
    poor: 'orange',
    broken: 'error',
  }
  return colors[condition] || 'grey'
}

function getConditionText(condition: string): string {
  return condition.charAt(0).toUpperCase() + condition.slice(1)
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
    month: 'long',
    day: 'numeric',
  })
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

