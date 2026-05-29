# Desktop Pet (Phase 2)

Electron transparent window shell for desktop pet mode.

## Prerequisites

- Frontend running at `http://localhost:5173` (or set `ASSISTANT_FRONTEND_URL`)
- Valid embed token in the URL

## Run

```bash
cd desktop
npm install
ASSISTANT_FRONTEND_URL="http://localhost:5173/embed/?token=YOUR_TOKEN" npm run dev
```

Full pet mode features (mouse pass-through, multi-monitor drag) will follow Open-LLM-VTuber-Web `window-manager.ts`.
