<template>
  <el-container class="main-layout">
    <el-aside width="220px" class="main-layout__aside">
      <div class="main-layout__brand">Live2D Assistant</div>
      <el-menu :default-active="activePath" router>
        <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
          {{ item.label }}
        </el-menu-item>
      </el-menu>
      <div class="main-layout__settings">
        <el-input
          v-model="apiKey"
          size="small"
          placeholder="Admin API Key"
          @change="saveApiKey"
        />
      </div>
    </el-aside>
    <el-main class="main-layout__main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useSettingsStore } from '@/store/settingsStore'

const route = useRoute()
const settings = useSettingsStore()
const apiKey = ref(settings.adminApiKey)

const menuItems = [
  { path: '/', label: '首页' },
  { path: '/admin/models', label: '模型管理' },
  { path: '/admin/preview', label: '模型预览' },
  { path: '/admin/characters', label: '角色画像' },
  { path: '/admin/embed', label: '嵌入管理' },
]

const activePath = computed(() => {
  if (route.path.startsWith('/chat')) return '/admin/characters'
  if (route.path.startsWith('/admin/preview')) return '/admin/preview'
  return route.path
})

function saveApiKey() {
  settings.setAdminApiKey(apiKey.value.trim())
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.main-layout__aside {
  background: #fff;
  border-right: 1px solid #ebeef5;
  display: flex;
  flex-direction: column;
}

.main-layout__brand {
  padding: 20px 16px;
  font-weight: 700;
  font-size: 16px;
}

.main-layout__settings {
  margin-top: auto;
  padding: 12px;
}

.main-layout__main {
  padding: 24px;
}
</style>
