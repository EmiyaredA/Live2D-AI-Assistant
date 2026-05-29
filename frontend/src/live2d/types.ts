export interface Live2DModelInfo {
  id?: number
  name?: string
  url?: string
  emotion_map?: Record<string, unknown>
  metadata?: Record<string, unknown>
}

export interface Live2DActions {
  expressions?: Array<number | string>
  motions?: string[]
}
