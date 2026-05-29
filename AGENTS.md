# AGENTS.md · Live2D-AI-Assistant

> AI 助手导航图。本文只介绍**目录结构与职责**；参考实现见各目录下的 `_template.py`（不参与运行，复制后合并到正式模块）。

## 项目是什么

**Live2D-AI-Assistant**：可自定义人设的 AI 助手，计划支持两种形态：

| 模式 | 说明 |
|------|------|
| **网站助手** | 浏览器 + WebSocket，语音/文字对话，Live2D 形象 |
| **桌面版** | 透明窗口、置顶、桌宠式陪伴（后续） |

能力方向（规划）：实时对话、TTS/ASR、Live2D 表情、可选工具调用（MCP）。可参考姊妹项目 [Open-LLM-VTuber](../Open-LLM-VTuber/) 的插件化思路，本仓库独立演进。

---

## 当前目录（仓库里实际有什么）

```text
Live2D-AI-Assistant/
├── AGENTS.md
├── ARCHITECTURE.md
├── README.md
├── _template.py                 # dev.py 参考模板
├── dev.py
├── .gitignore
└── backend/
    ├── _template.py             # app.py 参考模板
    ├── app.py
    ├── pyproject.toml
    ├── db/
    │   ├── _template.py         # db.py + models.py 参考模板
    │   ├── db.py
    │   ├── models.py
    │   └── schemas/
    │       └── _template.py     # API DTO 参考模板
    ├── api/
    │   └── _template.py
    ├── core/
    │   ├── _template.py
    │   └── tts/
    │       └── _template.py
    └── conversations/
        └── _template.py
```

**状态说明**：正式实现文件（`app.py`、`db.py` 等）多数仍为骨架；带 `_template` 前缀的文件仅供查阅与复制，不会被应用导入。

---

## 目标目录结构（推荐）

```text
Live2D-AI-Assistant/
├── dev.py                      # 一键启动：backend + frontend
├── frontend/                   # 网站助手 UI（Vue/React + Live2D）
│   └── src/
│       ├── pages/              # 对话页、设置页
│       ├── live2d/             # 模型加载、表情映射
│       └── api/                # WebSocket / REST 客户端
├── desktop/                    # 桌面壳（Electron/Tauri，后续）
├── prompts/                    # 人设与 system prompt 模板
├── live2d-models/              # Live2D 模型资源
├── config/                     # conf.yaml、角色配置
└── backend/
    ├── app.py
    ├── pyproject.toml
    ├── db/                     # 数据层
    ├── api/                    # HTTP / WebSocket 路由（薄）
    ├── core/                   # 业务逻辑（不感知 HTTP）
    │   ├── asr/
    │   ├── tts/
    │   ├── agent/
    │   └── live2d_model.py
    ├── conversations/          # 对话编排流水线
    └── tests/
```

---

## 分层职责

| 层级 | 路径 | 职责 | 不要放什么 |
|------|------|------|------------|
| 入口 | `app.py`、`dev.py` | 启动、中间件、注册路由 | 业务算法 |
| 传输 | `api/` | 鉴权、解析请求、调 `core`、返回 JSON/WS | 复杂领域逻辑 |
| 业务 | `core/`、`conversations/` | ASR/TTS/Agent/Live2D、对话流程 | 直接 `include_router` |
| 数据 | `db/` | 连接、ORM、迁移、API DTO | 调用大模型 |
| 资源 | `prompts/`、`live2d-models/`、`config/` | 静态配置与素材 | Python 业务代码 |
| 展示 | `frontend/`、`desktop/` | UI、Live2D 渲染 | 后端 secrets |

---

## 目录与功能说明

### 仓库根

| 路径 | 功能 | 模板 |
|------|------|------|
| `dev.py` | 开发环境：拉起后端与前端、可选热重载 | [_template.py](_template.py) |
| `config/` | `conf.yaml`、角色与引擎默认配置 | — |
| `prompts/` | 人设、`system` 与工具 prompt 文本 | — |
| `live2d-models/` | Live2D `.model3.json` 与贴图 | — |
| `frontend/` | 网站助手 UI | — |
| `desktop/` | 桌面透明窗/桌宠壳 | — |

### `backend/` — 后端根

| 路径 | 功能 | 模板 |
|------|------|------|
| `app.py` | FastAPI 应用：生命周期、`CORS`、挂路由、静态资源 | [_template.py](backend/_template.py) |
| `pyproject.toml` | 依赖、`uv`、测试与 lint 配置 | — |

### `backend/db/` — 数据层

| 路径 | 功能 | 模板 |
|------|------|------|
| `db.py` | `engine`、`get_session`、`init_db`、迁移入口 | 见 [_template.py](backend/db/_template.py) 前半（连接与会话） |
| `models.py` | `SQLModel, table=True` 表定义（角色、聊天记录等） | 见 [_template.py](backend/db/_template.py) 后半（ORM） |
| `schemas/` | Pydantic 请求/响应 DTO，与 ORM 分离 | [_template.py](backend/db/schemas/_template.py) |

**区分**：`models` 落库；`schemas` 描述 HTTP JSON，可省略敏感字段。

### `backend/api/` — 传输层

| 路径 | 功能 | 模板 |
|------|------|------|
| `chat.py`（规划） | REST 对话、配置查询 | [_template.py](backend/api/_template.py) |
| `websocket_handler.py`（规划） | WebSocket 消息分派、会话连接 | 实现时参考 Open-LLM-VTuber 同名模块 |

### `backend/core/` — 业务层

| 路径 | 功能 | 模板 |
|------|------|------|
| `settings.py`（规划） | `.env`、数据目录、CORS | — |
| `service_context.py`（规划） | 按配置组装 ASR / TTS / Agent / Live2D（会话级 DI） | [_template.py](backend/core/_template.py) |
| `live2d_model.py`（规划） | 表情 key 与模型元信息 | — |
| `asr/`（规划） | `ASRInterface` + `ASRFactory` + 各引擎实现 | — |
| `tts/`（规划） | `TTSInterface` + `TTSFactory` + 各引擎实现 | [_template.py](backend/core/tts/_template.py) |
| `agent/`（规划） | `AgentInterface` + 带记忆的对话 Agent | — |

### `backend/conversations/` — 对话编排

| 路径 | 功能 | 模板 |
|------|------|------|
| `single_conversation.py`（规划） | 单人一轮：ASR → Agent 流 → 分句/表情 → TTS → 推送 | [_template.py](backend/conversations/_template.py) |
| `conversation_handler.py`（规划） | 触发对话、打断 | — |

**主路径（规划）**：

```text
WebSocket → api/websocket_handler → conversations/single_conversation
  → core（ASR / Agent / TTS / Live2D）→ 回推前端
```

---

## 运行约定（目标）

在项目根目录执行：

```bash
uv sync
uv run dev.py
uv run pytest backend/tests/ -q
```

| 环境变量（规划） | 说明 |
|------------------|------|
| `ASSISTANT_DATA_DIR` | SQLite、缓存音频 |
| `ASSISTANT_HOST` / `ASSISTANT_PORT` | 后端监听 |
| LLM / TTS API Key | 按提供商配置，写入 `.env.example`，勿提交 `.env` |

---

## 任务路由

| 场景 | 优先改 | 参考模板 |
|------|--------|----------|
| 加/改数据库表 | `backend/db/models.py` | `backend/db/_template.py` |
| 改 API 入参/出参 | `backend/db/schemas/` | `backend/db/schemas/_template.py` |
| 换 TTS/ASR/LLM | `backend/core/*/factory` + `config/` | `backend/core/tts/_template.py` |
| 改对话流程 | `backend/conversations/` | `backend/conversations/_template.py` |
| 改 HTTP/WS 入口 | `backend/api/` | `backend/api/_template.py` |
| 改应用启动 | `backend/app.py`、`dev.py` | `backend/_template.py`、`_template.py` |
| 改 Live2D / 人设 | `core/live2d_model.py`、`prompts/` | — |
| 改页面 | `frontend/src/` | — |
| 架构总览 | [ARCHITECTURE.md](ARCHITECTURE.md) | — |

---

## 与 Open-LLM-VTuber 的对照

| Open-LLM-VTuber | 本仓库 |
|-----------------|--------|
| `service_context.py` | `backend/core/service_context.py` |
| `asr/` `tts/` `agent/` | `backend/core/` 下同结构 |
| `conversations/` | `backend/conversations/` |
| `prompts/` | 仓库根 `prompts/` |
| 文件历史为主 | `backend/db/` 存配置与聊天记录 |

---

## 约束

- 不提交 `.env`、密钥、本地 `data/` 库文件
- 业务写 `core/`，`api/` 保持薄层
- 结构变化时同步更新 [ARCHITECTURE.md](ARCHITECTURE.md) 与本文件
- `_template.py` 仅作参考，实现后勿从生产路径 `import` 模板文件

---

## 文档职责

| 文档 | 职责 |
|------|------|
| [README.md](README.md) | 人类快速上手 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 架构、主路径、模块图 |
| **AGENTS.md** | 目录、分层、改码落点、模板索引 |
