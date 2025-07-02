<template>
  <v-dialog v-model="dialog" max-width="500px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        Assign Asset
      </v-card-title>

      <v-card-text>
        <div class="mb-4">
          <h3>{{ asset?.name }}</h3>
          <p class="text-medium-emphasis">{{ asset?.asset_tag }}</p>
        </div>

        <v-form ref="form" v-model="valid">
          <v-select
            v-model="formData.assigned_to"
            :items="users"
            item-title="full_name"
            item-value="id"
            label="Assign to User *"
            :rules="[rules.required]"
            variant="outlined"
            density="compact"
          >
            <template #item="{ props, item }">
              <v-list-item v-bind="props">
                <template #prepend>
                  <v-avatar size="32">
                    <v-icon>mdi-account</v-icon>
                  </v-avatar>
                </template>
                <v-list-item-title>{{ item.raw.full_name }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.raw.email }}</v-list-item-subtitle>
              </v-list-item>
            </template>
          </v-select>

          <v-textarea
            v-model="formData.notes"
            label="Assignment Notes"
            variant="outlined"
            density="compact"
            rows="3"
            placeholder="Optional notes about this assignment..."
          />
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
          @click="assignAsset"
        >
          Assign
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { assetService, type Asset, type User } from '@/services/api'

interface Props {
  modelValue: boolean
  asset?: Asset | null
  users: User[]
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'assigned'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const form = ref()
const valid = ref(false)
const loading = ref(false)

const formData = ref({
  assigned_to: null as number | null,
  notes: '',
})

const rules = {
  required: (value: any) => !!value || 'This field is required',
}

async function assignAsset() {
  if (!valid.value || !props.asset || !formData.value.assigned_to) return

  loading.value = true
  try {
    await assetService.assign(props.asset.id, {
      assigned_to: formData.value.assigned_to,
      notes: formData.value.notes,
    })

    emit('assigned')
  } catch (error) {
    console.error('Error assigning asset:', error)
  } finally {
    loading.value = false
  }
}

function closeDialog() {
  dialog.value = false
  formData.value = {
    assigned_to: null,
    notes: '',
  }
}
</script>

