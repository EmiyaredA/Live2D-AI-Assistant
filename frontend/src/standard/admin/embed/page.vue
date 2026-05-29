<template>
  <div class="embed-page">
    <div class="page-header">
      <h2>嵌入管理</h2>
      <el-button type="primary" @click="openCreate">生成 Token</el-button>
    </div>

    <el-table :data="tokens" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="character_id" label="角色 ID" width="100" />
      <el-table-column prop="token" label="Token" show-overflow-tooltip />
      <el-table-column prop="allowed_origins" label="允许来源" width="140" />
      <el-table-column label="操作" width="260">
        <template #default="{ row }">
          <el-button size="small" @click="copySnippet(row.token)">复制 iframe</el-button>
          <el-button size="small" type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="生成嵌入 Token" width="480px">
      <el-form label-width="100px">
        <el-form-item label="角色">
          <el-select v-model="form.character_id" style="width: 100%">
            <el-option
              v-for="c in characterOptions"
              :key="c.id"
              :label="`${c.name} (#${c.id})`"
              :value="c.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="允许来源">
          <el-input v-model="form.allowed_origins" placeholder="* 或 https://example.com" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">生成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { listCharacters, type Character } from '@/api/characters'
import {
  buildIframeSnippet,
  createEmbedToken,
  deleteEmbedToken,
  listEmbedTokens,
  type EmbedToken,
} from '@/api/embed'
import { useSettingsStore } from '@/store/settingsStore'

const settings = useSettingsStore()
const tokens = ref<EmbedToken[]>([])
const characterOptions = ref<Character[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const form = reactive({ character_id: null as number | null, allowed_origins: '*' })

async function load() {
  loading.value = true
  try {
    ;[tokens.value, characterOptions.value] = await Promise.all([
      listEmbedTokens(settings.adminApiKey),
      listCharacters(),
    ])
  } catch {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.character_id = characterOptions.value[0]?.id ?? null
  form.allowed_origins = '*'
  dialogVisible.value = true
}

async function save() {
  if (!form.character_id) {
    ElMessage.warning('请选择角色')
    return
  }
  try {
    await createEmbedToken(settings.adminApiKey, {
      character_id: form.character_id,
      allowed_origins: form.allowed_origins,
    })
    dialogVisible.value = false
    await load()
    ElMessage.success('已生成')
  } catch {
    ElMessage.error('生成失败')
  }
}

async function remove(id: number) {
  await deleteEmbedToken(settings.adminApiKey, id)
  await load()
}

async function copySnippet(token: string) {
  const snippet = buildIframeSnippet(token)
  await navigator.clipboard.writeText(snippet)
  ElMessage.success('iframe 代码已复制')
}

onMounted(load)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
</style>
