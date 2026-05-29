<template>
  <div class="model-preview-panel">
    <div class="model-preview-panel__stage">
      <Live2DCanvas
        ref="canvasRef"
        inspect-mode
        :model-info="modelInfo"
        :actions="previewActions"
        :subtitle="previewSubtitle"
      />
    </div>

    <div class="model-preview-panel__sidebar">
      <h3 v-if="modelInfo?.name">{{ modelInfo.name }}</h3>
      <p v-if="description" class="model-preview-panel__desc">{{ description }}</p>

      <div class="model-preview-panel__inspect">
        <div class="model-preview-panel__section-title">视角检查</div>
        <p class="model-preview-panel__inspect-tip">
          在左侧画布拖拽可旋转 Live2D 视角，滚轮缩放。Live2D 为 2.5D 透视，非真 3D 模型。
        </p>
        <el-button size="small" @click="resetView">重置视角</el-button>
        <div class="model-preview-panel__zoom">
          <span class="model-preview-panel__zoom-label">缩放 {{ zoomLabel }}</span>
          <el-slider
            :model-value="zoomPercent"
            :min="20"
            :max="200"
            :step="5"
            @input="onZoomChange"
          />
        </div>
      </div>

      <el-descriptions :column="1" border size="small" class="model-preview-panel__meta">
        <el-descriptions-item label="模型路径">
          {{ modelPath || '—' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="modelInfo?.url" label="资源 URL">
          <el-link :href="modelInfo.url" target="_blank" type="primary">
            {{ modelInfo.url }}
          </el-link>
        </el-descriptions-item>
      </el-descriptions>

      <div v-if="emotionEntries.length" class="model-preview-panel__emotions">
        <div class="model-preview-panel__section-title">表情预览</div>
        <div class="model-preview-panel__chips">
          <el-tag
            v-for="[label, value] in emotionEntries"
            :key="label"
            :type="activeEmotion === label ? 'primary' : 'info'"
            class="model-preview-panel__chip"
            effect="plain"
            @click="selectEmotion(label, value)"
          >
            [{{ label }}] → {{ value }}
          </el-tag>
        </div>
      </div>

      <div v-else class="model-preview-panel__empty">
        暂无 emotion_map，可在模型管理中配置表情映射。
      </div>

      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import Live2DCanvas from '@/live2d/Live2DCanvas.vue'
import type { Live2DModelInfo } from '@/live2d/types'

const props = defineProps<{
  modelInfo: Live2DModelInfo | null
  modelPath?: string
}>()

const canvasRef = ref<InstanceType<typeof Live2DCanvas> | null>(null)
const activeEmotion = ref('')
const previewActions = ref<{ expressions: Array<number | string> } | null>(null)
const previewSubtitle = ref('')
const zoomPercent = ref(100)

const zoomLabel = computed(() => `${zoomPercent.value}%`)

const description = computed(() => {
  const meta = props.modelInfo?.metadata as Record<string, unknown> | undefined
  return (meta?.description as string) || ''
})

const emotionEntries = computed(() => {
  const map = props.modelInfo?.emotion_map || {}
  return Object.entries(map)
})

watch(
  () => props.modelInfo?.id,
  () => {
    activeEmotion.value = ''
    previewActions.value = null
    previewSubtitle.value = ''
    zoomPercent.value = 100
  },
)

function onZoomChange(value: number | number[]) {
  const v = Array.isArray(value) ? value[0] : value
  zoomPercent.value = v
  canvasRef.value?.setZoom(v / 100)
}

function selectEmotion(label: string, value: unknown) {
  activeEmotion.value = label
  previewActions.value = {
    expressions: [value as number | string],
  }
  previewSubtitle.value = `[${label}] 表情预览`
}

function resetView() {
  zoomPercent.value = 100
  canvasRef.value?.resetView()
}
</script>

<style scoped>
.model-preview-panel {
  display: grid;
  grid-template-columns: minmax(260px, 1fr) 300px;
  gap: 20px;
  min-height: 480px;
}

.model-preview-panel__stage {
  min-height: 400px;
  max-height: min(78vh, 680px);
  border: 1px solid #ebeef5;
  border-radius: 16px;
  overflow: hidden;
  background: #fff;
}

.model-preview-panel__sidebar h3 {
  margin: 0 0 8px;
}

.model-preview-panel__desc {
  margin: 0 0 12px;
  color: #606266;
  font-size: 14px;
  line-height: 1.5;
}

.model-preview-panel__inspect {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 10px;
  background: #f5f9ff;
}

.model-preview-panel__inspect-tip {
  margin: 0 0 10px;
  font-size: 12px;
  line-height: 1.5;
  color: #606266;
}

.model-preview-panel__zoom {
  margin-top: 12px;
}

.model-preview-panel__zoom-label {
  display: block;
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
}

.model-preview-panel__meta {
  margin-bottom: 16px;
}

.model-preview-panel__section-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #303133;
}

.model-preview-panel__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.model-preview-panel__chip {
  cursor: pointer;
  user-select: none;
}

.model-preview-panel__empty {
  color: #909399;
  font-size: 13px;
}

@media (max-width: 900px) {
  .model-preview-panel {
    grid-template-columns: 1fr;
  }
}
</style>
