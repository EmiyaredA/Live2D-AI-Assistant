<template>
  <div class="preview-page">
    <div class="page-header">
      <h2>模型预览</h2>
      <el-select
        v-model="selectedId"
        placeholder="选择模型"
        filterable
        style="width: 260px"
        @change="onSelectChange"
      >
        <el-option
          v-for="m in models"
          :key="m.id"
          :label="`${m.name} (#${m.id})`"
          :value="m.id"
        />
      </el-select>
    </div>

    <el-empty v-if="!models.length && !loading" description="暂无模型，请先在模型管理中创建" />

    <ModelPreviewPanel
      v-else-if="currentModel"
      :model-info="currentModelInfo"
      :model-path="currentModel.model_path"
    >
      <template #actions>
        <div class="preview-page__actions">
          <el-button @click="$router.push('/admin/models')">管理模型</el-button>
          <el-button type="primary" @click="goChatWithModel">
            创建角色并对话
          </el-button>
        </div>
      </template>
    </ModelPreviewPanel>

    <div v-else v-loading="loading" class="preview-page__loading" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { listLive2DModels, type Live2DModel } from '@/api/live2dModels'
import ModelPreviewPanel from '@/components/ModelPreviewPanel.vue'
import { toModelInfo } from '@/utils/live2dModel'

const route = useRoute()
const router = useRouter()
const models = ref<Live2DModel[]>([])
const loading = ref(false)
const selectedId = ref<number | null>(null)

const currentModel = computed(() =>
  models.value.find((m) => m.id === selectedId.value) ?? null,
)

const currentModelInfo = computed(() =>
  currentModel.value ? toModelInfo(currentModel.value) : null,
)

async function load() {
  loading.value = true
  try {
    models.value = await listLive2DModels()
    syncSelectionFromRoute()
  } catch {
    ElMessage.error('加载模型失败')
  } finally {
    loading.value = false
  }
}

function syncSelectionFromRoute() {
  const paramId = route.params.modelId
  if (paramId) {
    const id = Number(paramId)
    if (models.value.some((m) => m.id === id)) {
      selectedId.value = id
      return
    }
  }
  if (!selectedId.value && models.value.length) {
    selectedId.value = models.value[0].id
  }
}

function onSelectChange(id: number) {
  router.replace({ name: 'AdminPreviewModel', params: { modelId: String(id) } })
}

function goChatWithModel() {
  router.push({
    path: '/admin/characters',
    query: { previewModelId: String(selectedId.value) },
  })
}

watch(
  () => route.params.modelId,
  () => syncSelectionFromRoute(),
)

onMounted(load)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.preview-page__actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.preview-page__loading {
  min-height: 320px;
}
</style>
