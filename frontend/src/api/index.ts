import axios from 'axios'
import { useSettingsStore } from '@/store/settingsStore'

export const apiClient = axios.create({
  timeout: 60000,
})

apiClient.interceptors.request.use((config) => {
  const settings = useSettingsStore()
  config.headers['X-Admin-API-Key'] = settings.adminApiKey
  return config
})

export function getWsBaseUrl(): string {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  return `${protocol}//${window.location.host}/api/ws/client-ws`
}
