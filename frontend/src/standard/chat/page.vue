<template>
  <div class="chat-page" :class="{ 'chat-page--standalone': standalone }">
    <div class="chat-page__live2d">
      <Live2DCanvas
        :model-info="character.modelInfo"
        :subtitle="chat.displayText"
        :actions="{ expressions: chat.lastExpressions }"
      />
    </div>
    <div class="chat-page__panel">
      <div class="chat-page__header">
        <h3>{{ character.characterName || '对话' }}</h3>
        <el-tag v-if="chat.connected" type="success" size="small">已连接</el-tag>
      </div>
      <ChatPanel :on-send="handleSend" :on-interrupt="handleInterrupt" />
    </div>
    <audio ref="audioRef" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ChatWebSocket } from '@/api/chat'
import ChatPanel from '@/components/ChatPanel.vue'
import Live2DCanvas from '@/live2d/Live2DCanvas.vue'
import { useCharacterStore } from '@/store/characterStore'
import { useChatStore } from '@/store/chatStore'

const props = defineProps<{
  characterId?: number
  embedToken?: string
}>()

const route = useRoute()
const character = useCharacterStore()
const chat = useChatStore()
const audioRef = ref<HTMLAudioElement | null>(null)
let ws: ChatWebSocket | null = null

const standalone = computed(() => Boolean(route.meta.standalone))

const resolvedCharacterId = computed(() => {
  if (props.characterId) return props.characterId
  const param = route.params.characterId
  return param ? Number(param) : undefined
})

function handleWsMessage(data: Record<string, unknown>) {
  const type = data.type as string
  if (type === 'set-model-and-conf') {
    character.setFromWs(data)
    chat.setConnected(true)
    return
  }
  if (type === 'display-text') {
    chat.setDisplayText((data.text as string) || '')
    const actions = data.actions as { expressions?: Array<number | string> } | undefined
    if (actions?.expressions) chat.setExpressions(actions.expressions)
    return
  }
  if (type === 'audio') {
    const display = data.display_text as { text?: string } | undefined
    const text = display?.text || ''
    if (text) chat.setDisplayText(text)
    const actions = data.actions as { expressions?: Array<number | string> } | undefined
    if (actions?.expressions) chat.setExpressions(actions.expressions)

    const audioB64 = data.audio as string | null
    if (audioB64 && audioRef.value) {
      audioRef.value.src = `data:audio/mp3;base64,${audioB64}`
      audioRef.value.play().catch(() => {})
    }
    return
  }
  if (type === 'turn-complete') {
    chat.finalizeAiMessage((data.text as string) || chat.displayText)
    return
  }
  if (type === 'error') {
    ElMessage.error((data.message as string) || '连接错误')
    chat.setLoading(false)
  }
}

function connect() {
  chat.clear()
  character.reset()
  ws = new ChatWebSocket(handleWsMessage)
  ws.connect()
  ws.fetchCharacter({
    characterId: resolvedCharacterId.value,
    embedToken: props.embedToken,
  })
}

function handleSend(text: string) {
  ws?.sendText(text, character.historyUid)
}

function handleInterrupt() {
  ws?.interrupt()
}

onMounted(connect)
onUnmounted(() => {
  ws?.close()
  ws = null
})
</script>

<style scoped>
.chat-page {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 16px;
  min-height: calc(100vh - 120px);
}

.chat-page--standalone {
  min-height: 100vh;
  padding: 12px;
  box-sizing: border-box;
  background: #f5f7fa;
}

.chat-page__live2d {
  min-height: 480px;
}

.chat-page__panel {
  display: flex;
  flex-direction: column;
  min-height: 480px;
}

.chat-page__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.chat-page__header h3 {
  margin: 0;
}

@media (max-width: 900px) {
  .chat-page {
    grid-template-columns: 1fr;
  }
}
</style>
