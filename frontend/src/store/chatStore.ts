import { defineStore } from 'pinia'

export interface ChatMessage {
  role: 'human' | 'ai'
  content: string
}

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as ChatMessage[],
    displayText: '',
    connected: false,
    loading: false,
    lastExpressions: [] as Array<number | string>,
  }),
  actions: {
    addHumanMessage(text: string) {
      this.messages.push({ role: 'human', content: text })
    },
    setDisplayText(text: string) {
      this.displayText = text
    },
    finalizeAiMessage(text: string) {
      if (text) {
        this.messages.push({ role: 'ai', content: text })
      }
      this.displayText = ''
      this.loading = false
    },
    setExpressions(expressions: Array<number | string>) {
      this.lastExpressions = expressions
    },
    setConnected(v: boolean) {
      this.connected = v
    },
    setLoading(v: boolean) {
      this.loading = v
    },
    clear() {
      this.messages = []
      this.displayText = ''
      this.loading = false
      this.lastExpressions = []
    },
  },
})
