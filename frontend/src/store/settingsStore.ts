import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    adminApiKey: localStorage.getItem('adminApiKey') || 'dev-admin-key',
  }),
  actions: {
    setAdminApiKey(key: string) {
      this.adminApiKey = key
      localStorage.setItem('adminApiKey', key)
    },
  },
})
