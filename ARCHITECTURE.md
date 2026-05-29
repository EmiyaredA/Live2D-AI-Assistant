# Live2D-AI-Assistant Architecture

## Overview

Self-hosted Live2D AI assistant platform with:

- Admin UI for Live2D models, character personas, and embed tokens
- Full-screen chat page with WebSocket dialogue
- iframe embed widget for third-party sites
- Phase 2: Electron desktop pet, full MCP runtime, JWT multi-tenant auth

## Layering

```text
frontend (Vue3) ──WebSocket/REST──► api/ ──► conversations/ ──► core/
                                              └── db/
```

| Layer | Responsibility |
|-------|----------------|
| `api/` | HTTP/WS transport, auth headers, thin routing |
| `conversations/` | Dialogue orchestration pipeline |
| `core/` | ASR/TTS/Agent/Live2D/MCP/Skill plugins |
| `db/` | SQLModel ORM + Pydantic schemas |
| `frontend/` | UI, Live2D canvas, embed entry |

## Main dialogue path

```text
WS text-input
  → websocket_handler
  → conversation_handler
  → single_conversation
      → agent.chat() stream
      → emotion extraction
      → TTS per sentence
      → WS display-text / audio / actions
```

## WebSocket messages (MVP)

**Client → Server**

- `fetch-character` — load character + Live2D model into session
- `text-input` — send user message
- `interrupt-signal` — cancel current generation

**Server → Client**

- `set-model-and-conf` — character and model metadata
- `display-text` — streaming subtitle
- `audio` — base64 MP3 + display_text + actions
- `error`

## Embed flow

1. Admin creates character and embed token (`POST /v1/embed-tokens`)
2. Copy iframe snippet from admin UI
3. Embed page loads `GET /v1/embed/preview?token=...`
4. WebSocket connects with `embed_token` in `fetch-character`

## Multi-tenant reservation

All primary tables include `tenant_id` (default `1`). Phase 2 adds JWT login and tenant-scoped API keys.

## Phase 2

- `desktop/` — Electron transparent window (pet mode)
- `core/mcp/` — MCP server registry and tool execution
- `core/skills/` — SKILL.md loader per character
