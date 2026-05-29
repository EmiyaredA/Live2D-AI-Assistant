import { getWsBaseUrl } from '@/api/index'

export type WSMessageHandler = (data: Record<string, unknown>) => void

export class ChatWebSocket {
  private ws: WebSocket | null = null
  private handler: WSMessageHandler

  constructor(handler: WSMessageHandler) {
    this.handler = handler
  }

  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) return
    this.ws = new WebSocket(getWsBaseUrl())
    this.ws.onmessage = (event) => {
      try {
        this.handler(JSON.parse(event.data))
      } catch {
        // ignore malformed messages
      }
    }
  }

  send(payload: Record<string, unknown>): void {
    if (this.ws?.readyState !== WebSocket.OPEN) {
      this.connect()
      this.ws!.onopen = () => this.ws?.send(JSON.stringify(payload))
      return
    }
    this.ws.send(JSON.stringify(payload))
  }

  fetchCharacter(opts: {
    characterId?: number
    embedToken?: string
    historyUid?: string
  }): void {
    this.send({
      type: 'fetch-character',
      character_id: opts.characterId,
      embed_token: opts.embedToken,
      history_uid: opts.historyUid,
    })
  }

  sendText(text: string, historyUid?: string): void {
    this.send({ type: 'text-input', text, history_uid: historyUid })
  }

  interrupt(): void {
    this.send({ type: 'interrupt-signal' })
  }

  close(): void {
    this.ws?.close()
    this.ws = null
  }
}
