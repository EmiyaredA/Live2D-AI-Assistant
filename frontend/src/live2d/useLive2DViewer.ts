import { onBeforeUnmount, ref, shallowRef, watch, type Ref } from 'vue'
import * as PIXI from 'pixi.js'
import {
  applyModelExpression,
  loadLive2DModel,
  setModelParameter,
  type PixiLive2DModel,
} from '@/live2d/live2dRuntime'
import type { Live2DModelInfo } from '@/live2d/types'

export interface Live2DViewerOptions {
  container: Ref<HTMLElement | null>
  modelInfo: Ref<Live2DModelInfo | null | undefined>
  inspectMode?: Ref<boolean>
  onStatus?: (message: string) => void
}

const DEFAULT_ANGLES = { x: 0, y: 0, z: 0, body: 0 }
const FIT_PADDING = 0.82
const MIN_ZOOM = 0.2
const MAX_ZOOM = 2.0

export function useLive2DViewer(options: Live2DViewerOptions) {
  const loading = ref(false)
  const error = ref('')
  const zoom = ref(1)
  const fitScale = ref(0.2)

  const appRef = shallowRef<PIXI.Application | null>(null)
  const modelRef = shallowRef<PixiLive2DModel | null>(null)

  let angles = { ...DEFAULT_ANGLES }
  let dragging = false
  let lastX = 0
  let lastY = 0
  let resizeObserver: ResizeObserver | null = null

  function report(msg: string) {
    options.onStatus?.(msg)
  }

  function applyAngles() {
    const model = modelRef.value
    if (!model) return
    setModelParameter(model, 'ParamAngleX', angles.x)
    setModelParameter(model, 'ParamAngleY', angles.y)
    setModelParameter(model, 'ParamAngleZ', angles.z)
    setModelParameter(model, 'ParamBodyAngleX', angles.body)
  }

  function measureFitScale(model: PixiLive2DModel, app: PIXI.Application): number {
    const prevScale = model.scale.x
    model.scale.set(1)
    model.updateTransform()

    const width = Math.max(model.width, 1)
    const height = Math.max(model.height, 1)
    const scaleX = (app.screen.width * FIT_PADDING) / width
    const scaleY = (app.screen.height * FIT_PADDING) / height
    const computed = Math.min(scaleX, scaleY)

    model.scale.set(prevScale)
    return Math.min(computed, 0.35)
  }

  function layoutModel() {
    const app = appRef.value
    const model = modelRef.value
    if (!app || !model) return

    model.x = app.screen.width / 2
    model.y = app.screen.height / 2
    model.anchor.set(0.5, 0.5)
    model.scale.set(fitScale.value * zoom.value)
  }

  function refit() {
    const app = appRef.value
    const model = modelRef.value
    if (!app || !model) return
    fitScale.value = measureFitScale(model, app)
    layoutModel()
  }

  function onPointerDown(event: PointerEvent) {
    if (!options.inspectMode?.value) return
    dragging = true
    lastX = event.clientX
    lastY = event.clientY
  }

  function onPointerMove(event: PointerEvent) {
    if (!dragging || !modelRef.value) return
    const dx = event.clientX - lastX
    const dy = event.clientY - lastY
    lastX = event.clientX
    lastY = event.clientY

    angles.x = clamp(angles.x + dx * 0.2, -30, 30)
    angles.y = clamp(angles.y - dy * 0.2, -30, 30)
    angles.body = clamp(angles.body + dx * 0.06, -10, 10)
    applyAngles()
  }

  function onPointerUp() {
    dragging = false
  }

  function onWheel(event: WheelEvent) {
    if (!options.inspectMode?.value) return
    event.preventDefault()
    const delta = event.deltaY > 0 ? -0.08 : 0.08
    zoom.value = clamp(zoom.value + delta, MIN_ZOOM, MAX_ZOOM)
    layoutModel()
  }

  function bindInspectEvents(el: HTMLElement) {
    el.addEventListener('pointerdown', onPointerDown)
    window.addEventListener('pointermove', onPointerMove)
    window.addEventListener('pointerup', onPointerUp)
    el.addEventListener('wheel', onWheel, { passive: false })

    resizeObserver = new ResizeObserver(() => {
      refit()
    })
    resizeObserver.observe(el)
  }

  function unbindInspectEvents(el: HTMLElement) {
    el.removeEventListener('pointerdown', onPointerDown)
    window.removeEventListener('pointermove', onPointerMove)
    window.removeEventListener('pointerup', onPointerUp)
    el.removeEventListener('wheel', onWheel)
    resizeObserver?.disconnect()
    resizeObserver = null
  }

  async function mount() {
    const container = options.container.value
    const info = options.modelInfo.value
    if (!container || !info?.url) return

    await destroy()
    loading.value = true
    error.value = ''
    report('正在加载 Live2D 模型…')

    try {
      const app = new PIXI.Application({
        backgroundAlpha: 0,
        resizeTo: container,
        antialias: true,
        autoDensity: true,
        resolution: Math.min(window.devicePixelRatio || 1, 2),
      })
      container.appendChild(app.view as HTMLCanvasElement)
      appRef.value = app

      const model = await loadLive2DModel(info.url)
      modelRef.value = model
      app.stage.addChild(model)

      zoom.value = 1
      angles = { ...DEFAULT_ANGLES }
      refit()
      applyAngles()

      try {
        await model.motion('Idle', 0)
      } catch {
        // 部分模型无 Idle 动作组
      }

      bindInspectEvents(container)
      report(options.inspectMode?.value ? '拖拽旋转 · 滚轮缩放 · 可继续缩小' : '')
    } catch (e) {
      error.value = e instanceof Error ? e.message : '模型加载失败'
      report('')
    } finally {
      loading.value = false
    }
  }

  async function destroy() {
    const container = options.container.value
    if (container) unbindInspectEvents(container)

    modelRef.value?.destroy()
    modelRef.value = null

    const app = appRef.value
    if (app) {
      app.destroy(true, { children: true, texture: true, baseTexture: true })
      appRef.value = null
      container?.replaceChildren()
    }
  }

  function resetView() {
    angles = { ...DEFAULT_ANGLES }
    zoom.value = 1
    applyAngles()
    refit()
  }

  function setZoom(value: number) {
    zoom.value = clamp(value, MIN_ZOOM, MAX_ZOOM)
    layoutModel()
  }

  async function playExpression(expression: number | string) {
    if (!modelRef.value) return
    await applyModelExpression(modelRef.value, expression)
  }

  watch(
    () => options.modelInfo.value?.url,
    () => {
      void mount()
    },
  )

  onBeforeUnmount(() => {
    void destroy()
  })

  return {
    loading,
    error,
    zoom,
    mount,
    destroy,
    resetView,
    setZoom,
    playExpression,
  }
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value))
}
