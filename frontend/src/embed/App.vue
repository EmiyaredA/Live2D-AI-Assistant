<template>
  <ChatPage v-if="token" :embed-token="token" />
  <div v-else class="embed-error">缺少 embed token，请使用 ?token=xxx</div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ChatPage from '@/standard/chat/page.vue'

const token = computed(() => new URLSearchParams(window.location.search).get('token') || '')
</script>

<style scoped>
.embed-error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #909399;
}
</style>
