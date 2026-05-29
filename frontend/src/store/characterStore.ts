import { defineStore } from 'pinia'

export interface ModelInfo {
  id?: number
  name?: string
  url?: string
  emotion_map?: Record<string, unknown>
  metadata?: Record<string, unknown>
}

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characterId: null as number | null,
    characterName: '',
    modelInfo: null as ModelInfo | null,
    historyUid: '',
  }),
  actions: {
    setFromWs(payload: Record<string, unknown>) {
      this.characterId = (payload.character_id as number) ?? null
      this.characterName = (payload.character_name as string) || ''
      this.modelInfo = (payload.model_info as ModelInfo) || null
      this.historyUid = (payload.history_uid as string) || ''
    },
    reset() {
      this.characterId = null
      this.characterName = ''
      this.modelInfo = null
      this.historyUid = ''
    },
  },
})
