<template>
  <v-dialog v-model="dialog" max-width="800px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        {{ isEdit ? 'Edit Asset' : 'Create New Asset' }}
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.asset_tag"
                label="Asset Tag *"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.name"
                label="Asset Name *"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="formData.description"
                label="Description"
                variant="outlined"
                density="compact"
                rows="3"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.category"
                :items="categories"
                item-title="name"
                item-value="id"
                label="Category *"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.location"
                :items="locations"
                item-title="name"
                item-value="id"
                label="Location *"
                :rules="[rules.required]"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.brand"
                label="Brand"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.model"
                label="Model"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.serial_number"
                label="Serial Number"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.status"
                :items="statusOptions"
                label="Status"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.condition"
                :items="conditionOptions"
                label="Condition"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="formData.vendor"
                :items="vendors"
                item-title="name"
                item-value="id"
                label="Vendor"
                variant="outlined"
                density="compact"
                clearable
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.qr_code"
                label="QR Code / Barcode"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.purchase_date"
                label="Purchase Date"
                type="date"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.purchase_cost"
                label="Purchase Cost"
                type="number"
                prefix="$"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="formData.invoice_number"
                label="Invoice Number"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.warranty_start_date"
                label="Warranty Start Date"
                type="date"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.warranty_end_date"
                label="Warranty End Date"
                type="date"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.warranty_provider"
                label="Warranty Provider"
                variant="outlined"
                density="compact"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="formData.useful_life_years"
                label="Useful Life (Years)"
                type="number"
                variant="outlined"
                density="compact"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12">
              <v-textarea
                v-model="formData.notes"
                label="Notes"
                variant="outlined"
                density="compact"
                rows="3"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          text
          @click="closeDialog"
        >
          Cancel
        </v-btn>
        <v-btn
          color="primary"
          :loading="loading"
          :disabled="!valid"
          @click="saveAsset"
        >
          {{ isEdit ? 'Update' : 'Create' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { assetService, type Asset, type AssetCategory, type Location, type Vendor } from '@/services/api'

interface Props {
  modelValue: boolean
  asset?: Asset | null
  categories: AssetCategory[]
  locations: Location[]
  vendors: Vendor[]
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'saved'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.asset?.id)
const form = ref()
const valid = ref(false)
const loading = ref(false)

const formData = ref({
  asset_tag: '',
  name: '',
  description: '',
  category: null as number | null,
  location: null as number | null,
  brand: '',
  model: '',
  serial_number: '',
  status: 'available',
  condition: 'good',
  vendor: null as number | null,
  qr_code: '',
  purchase_date: '',
  purchase_cost: '',
  invoice_number: '',
  warranty_start_date: '',
  warranty_end_date: '',
  warranty_provider: '',
  useful_life_years: 3,
  notes: '',
})

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

const conditionOptions = [
  { title: 'Excellent', value: 'excellent' },
  { title: 'Good', value: 'good' },
  { title: 'Fair', value: 'fair' },
  { title: 'Poor', value: 'poor' },
  { title: 'Broken', value: 'broken' },
]

const rules = {
  required: (value: any) => !!value || 'This field is required',
}

watch(() => props.asset, (newAsset) => {
  if (newAsset) {
    // Populate form with asset data for editing
    formData.value = {
      asset_tag: newAsset.asset_tag || '',
      name: newAsset.name || '',
      description: newAsset.description || '',
      category: newAsset.category || null,
      location: newAsset.location || null,
      brand: newAsset.brand || '',
      model: newAsset.model || '',
      serial_number: newAsset.serial_number || '',
      status: newAsset.status || 'available',
      condition: newAsset.condition || 'good',
      vendor: newAsset.vendor || null,
      qr_code: newAsset.qr_code || '',
      purchase_date: newAsset.purchase_date || '',
      purchase_cost: newAsset.purchase_cost || '',
      invoice_number: newAsset.invoice_number || '',
      warranty_start_date: newAsset.warranty_start_date || '',
      warranty_end_date: newAsset.warranty_end_date || '',
      warranty_provider: newAsset.warranty_provider || '',
      useful_life_years: newAsset.useful_life_years || 3,
      notes: newAsset.notes || '',
    }
  } else {
    // Reset form for new asset
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  formData.value = {
    asset_tag: '',
    name: '',
    description: '',
    category: null,
    location: null,
    brand: '',
    model: '',
    serial_number: '',
    status: 'available',
    condition: 'good',
    vendor: null,
    qr_code: '',
    purchase_date: '',
    purchase_cost: '',
    invoice_number: '',
    warranty_start_date: '',
    warranty_end_date: '',
    warranty_provider: '',
    useful_life_years: 3,
    notes: '',
  }
}

async function saveAsset() {
  if (!valid.value) return

  loading.value = true
  try {
    const data = {
      ...formData.value,
      purchase_cost: formData.value.purchase_cost ? parseFloat(formData.value.purchase_cost) : null,
    }

    if (isEdit.value && props.asset) {
      await assetService.update(props.asset.id, data)
    } else {
      await assetService.create(data)
    }

    emit('saved')
  } catch (error) {
    console.error('Error saving asset:', error)
  } finally {
    loading.value = false
  }
}

function closeDialog() {
  dialog.value = false
  resetForm()
}
</script>

