<template>
  <div class="live2d-canvas">
    <div
      ref="containerRef"
      class="live2d-canvas__stage"
      :class="{ 'live2d-canvas__stage--inspect': inspectMode }"
    >
      <div v-if="loading" class="live2d-canvas__overlay">加载 Live2D 模型…</div>
      <div v-else-if="error" class="live2d-canvas__overlay live2d-canvas__overlay--error">
        {{ error }}
      </div>
      <div v-if="currentExpression" class="live2d-canvas__expression">
        {{ currentExpression }}
      </div>
      <div v-if="inspectMode && statusText" class="live2d-canvas__hint">{{ statusText }}</div>
    </div>
    <p v-if="subtitle" class="live2d-canvas__subtitle">{{ subtitle }}</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, toRef, watch } from 'vue'
import { applyExpressions, expressionLabel } from '@/live2d/emotionMapper'
import { useLive2DViewer } from '@/live2d/useLive2DViewer'
import type { Live2DActions, Live2DModelInfo } from '@/live2d/types'

const props = withDefaults(
  defineProps<{
    modelInfo?: Live2DModelInfo | null
    subtitle?: string
    actions?: Live2DActions | null
    inspectMode?: boolean
  }>(),
  {
    inspectMode: false,
  },
)

const emit = defineEmits<{
  ready: []
  error: [message: string]
}>()

const containerRef = ref<HTMLElement | null>(null)
const currentExpression = ref('')
const statusText = ref('')

const modelInfoRef = ref(props.modelInfo)
watch(
  () => props.modelInfo,
  (v) => {
    modelInfoRef.value = v
  },
)

const { loading, error, mount, playExpression, resetView, setZoom, zoom } = useLive2DViewer({
  container: containerRef,
  modelInfo: modelInfoRef,
  inspectMode: toRef(props, 'inspectMode'),
  onStatus: (msg) => {
    statusText.value = msg
  },
})

watch(error, (msg) => {
  if (msg) emit('error', msg)
})

watch(loading, (v, prev) => {
  if (prev && !v && !error.value) emit('ready')
})

watch(
  () => props.actions,
  (actions) => {
    applyExpressions(actions, async (expr) => {
      const map = props.modelInfo?.emotion_map || {}
      currentExpression.value = expressionLabel(expr, map)
      await playExpression(expr)
    })
  },
  { deep: true },
)

onMounted(async () => {
  await mount()
})

defineExpose({ resetView, playExpression, setZoom, zoom })
</script>

<style scoped>
.live2d-canvas {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  height: 100%;
}

.live2d-canvas__stage {
  position: relative;
  flex: 1;
  width: 100%;
  min-height: 280px;
  max-height: min(72vh, 640px);
  background: radial-gradient(circle at 50% 20%, #eef5ff 0%, #f8fbff 55%, #edf2f7 100%);
  border-radius: 16px;
  overflow: hidden;
}

.live2d-canvas__stage--inspect {
  cursor: grab;
  touch-action: none;
}

.live2d-canvas__stage--inspect:active {
  cursor: grabbing;
}

.live2d-canvas__stage :deep(canvas) {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

.live2d-canvas__overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #606266;
  background: rgba(255, 255, 255, 0.55);
  z-index: 2;
  pointer-events: none;
}

.live2d-canvas__overlay--error {
  color: #f56c6c;
  padding: 16px;
  text-align: center;
}

.live2d-canvas__expression {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(64, 158, 255, 0.92);
  color: #fff;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  z-index: 3;
  pointer-events: none;
}

.live2d-canvas__hint {
  position: absolute;
  left: 12px;
  bottom: 12px;
  background: rgba(0, 0, 0, 0.45);
  color: #fff;
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 12px;
  z-index: 3;
  pointer-events: none;
}

.live2d-canvas__subtitle {
  margin: 12px 0 0;
  min-height: 24px;
  color: #303133;
  text-align: center;
}
</style>
