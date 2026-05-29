<template>
  <div class="chat-panel">
    <div class="chat-panel__messages" ref="listRef">
      <div
        v-for="(msg, idx) in chat.messages"
        :key="idx"
        class="chat-panel__message"
        :class="`chat-panel__message--${msg.role}`"
      >
        {{ msg.content }}
      </div>
      <div v-if="chat.displayText" class="chat-panel__message chat-panel__message--ai streaming">
        {{ chat.displayText }}
      </div>
    </div>
    <div class="chat-panel__input">
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="2"
        placeholder="输入消息..."
        @keydown.enter.exact.prevent="send"
      />
      <div class="chat-panel__actions">
        <el-button :disabled="!chat.loading" @click="interrupt">打断</el-button>
        <el-button type="primary" :loading="chat.loading" @click="send">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useChatStore } from '@/store/chatStore'

const props = defineProps<{
  onSend: (text: string) => void
  onInterrupt: () => void
}>()

const chat = useChatStore()
const inputText = ref('')
const listRef = ref<HTMLElement | null>(null)

async function send() {
  const text = inputText.value.trim()
  if (!text || chat.loading) return
  inputText.value = ''
  chat.addHumanMessage(text)
  chat.setLoading(true)
  props.onSend(text)
}

function interrupt() {
  props.onInterrupt()
  chat.setLoading(false)
}

watch(
  () => [chat.messages.length, chat.displayText],
  async () => {
    await nextTick()
    if (listRef.value) {
      listRef.value.scrollTop = listRef.value.scrollHeight
    }
  },
)
</script>

<style scoped>
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #ebeef5;
}

.chat-panel__messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.chat-panel__message {
  margin-bottom: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  max-width: 85%;
  white-space: pre-wrap;
}

.chat-panel__message--human {
  margin-left: auto;
  background: #409eff;
  color: #fff;
}

.chat-panel__message--ai,
.chat-panel__message.streaming {
  background: #f4f4f5;
  color: #303133;
}

.chat-panel__input {
  padding: 12px;
  border-top: 1px solid #ebeef5;
}

.chat-panel__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>
