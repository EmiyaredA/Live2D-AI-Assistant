import { apiClient } from '@/api/index'

export interface Live2DModel {
  id: number
  tenant_id: number
  name: string
  model_path: string
  emotion_map: Record<string, unknown>
  metadata: Record<string, unknown>
  created_at: number
}

export interface Live2DModelCreate {
  name: string
  model_path?: string
  emotion_map?: Record<string, unknown>
  metadata?: Record<string, unknown>
}

export async function listLive2DModels(): Promise<Live2DModel[]> {
  const { data } = await apiClient.get<Live2DModel[]>('/v1/live2d-models')
  return data
}

export async function createLive2DModel(body: Live2DModelCreate): Promise<Live2DModel> {
  const { data } = await apiClient.post<Live2DModel>('/v1/live2d-models', body)
  return data
}

export async function updateLive2DModel(
  id: number,
  body: Partial<Live2DModelCreate>,
): Promise<Live2DModel> {
  const { data } = await apiClient.patch<Live2DModel>(`/v1/live2d-models/${id}`, body)
  return data
}

export async function deleteLive2DModel(id: number): Promise<void> {
  await apiClient.delete(`/v1/live2d-models/${id}`)
}

export async function uploadModelFile(id: number, file: File): Promise<Live2DModel> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await apiClient.post<Live2DModel>(`/v1/live2d-models/${id}/upload`, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function getModelInfo(id: number) {
  const { data } = await apiClient.get(`/v1/live2d-models/${id}/info`)
  return data
}
