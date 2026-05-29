import { apiClient } from '@/api/index'

export interface Character {
  id: number
  tenant_id: number
  name: string
  persona_prompt: string
  live2d_model_id: number | null
  llm_config: Record<string, unknown>
  tts_config: Record<string, unknown>
  asr_config: Record<string, unknown>
  mcp_config: Record<string, unknown>
  skill_ids: string[]
  created_at: number
}

export interface CharacterCreate {
  name: string
  persona_prompt?: string
  live2d_model_id?: number | null
  llm_config?: Record<string, unknown>
  tts_config?: Record<string, unknown>
}

export async function listCharacters(): Promise<Character[]> {
  const { data } = await apiClient.get<Character[]>('/v1/characters')
  return data
}

export async function createCharacter(body: CharacterCreate): Promise<Character> {
  const { data } = await apiClient.post<Character>('/v1/characters', body)
  return data
}

export async function updateCharacter(
  id: number,
  body: Partial<CharacterCreate>,
): Promise<Character> {
  const { data } = await apiClient.patch<Character>(`/v1/characters/${id}`, body)
  return data
}

export async function deleteCharacter(id: number): Promise<void> {
  await apiClient.delete(`/v1/characters/${id}`)
}
