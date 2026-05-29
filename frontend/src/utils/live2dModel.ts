import type { Live2DModel } from '@/api/live2dModels'
import type { Live2DModelInfo } from '@/live2d/types'

export function toModelInfo(
  model: Live2DModel | {
    id: number
    name: string
    url?: string
    emotion_map?: Record<string, unknown>
    metadata?: Record<string, unknown>
  },
): Live2DModelInfo {
  const url =
    'url' in model && model.url
      ? model.url
      : 'model_path' in model && model.model_path
        ? `/live2d-models/${String(model.model_path).replace(/^\//, '')}`
        : ''

  return {
    id: model.id,
    name: model.name,
    url,
    emotion_map: model.emotion_map || {},
    metadata: model.metadata || {},
  }
}
