import axios from 'axios'

export interface EmbedToken {
  id: number
  character_id: number
  token: string
  allowed_origins: string
  expires_at: number | null
  created_at: number
}

export interface EmbedPreview {
  character_id: number
  character_name: string
  persona_prompt: string
  live2d_model: Record<string, unknown> | null
  ws_url: string
}

export async function listEmbedTokens(adminApiKey: string): Promise<EmbedToken[]> {
  const { data } = await axios.get<EmbedToken[]>('/v1/embed-tokens', {
    headers: { 'X-Admin-API-Key': adminApiKey },
  })
  return data
}

export async function createEmbedToken(
  adminApiKey: string,
  body: { character_id: number; allowed_origins?: string },
): Promise<EmbedToken> {
  const { data } = await axios.post<EmbedToken>('/v1/embed-tokens', body, {
    headers: { 'X-Admin-API-Key': adminApiKey },
  })
  return data
}

export async function deleteEmbedToken(adminApiKey: string, tokenId: number): Promise<void> {
  await axios.delete(`/v1/embed-tokens/${tokenId}`, {
    headers: { 'X-Admin-API-Key': adminApiKey },
  })
}

export async function fetchEmbedPreview(token: string): Promise<EmbedPreview> {
  const { data } = await axios.get<EmbedPreview>('/v1/embed/preview', {
    params: { token },
  })
  return data
}

export function buildIframeSnippet(token: string, origin = window.location.origin): string {
  return `<iframe src="${origin}/embed/?token=${token}" style="width:380px;height:600px;border:none;border-radius:12px" allow="microphone"></iframe>`
}
