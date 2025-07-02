import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('authToken'))
  const user = ref<any>(null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('authToken', newToken)
  }

  function setUser(userData: any) {
    user.value = userData
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('authToken')
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    setUser,
    logout,
  }
})

