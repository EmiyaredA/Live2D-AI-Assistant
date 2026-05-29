# Live2D-AI-Assistant

可自定义人设与 Live2D 形象的 AI 助手平台，支持网站助手与 iframe 嵌入；桌宠模式见 Phase 2。

## 快速开始

```bash
# 后端依赖
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY

uv sync --extra dev

# 前端依赖
cd frontend && npm install && cd ..

# 可选：从 Open-LLM-VTuber 链接示例 Live2D 模型（mao_pro、shizuku）
uv run python scripts/link_olv_models.py

# 一键启动（后端 8000 + 前端 5173）
uv run dev.py
```

- 管理后台：http://localhost:5173
- **模型预览**：侧栏「模型预览」— 真实 Live2D 渲染，支持拖拽旋转视角、滚轮缩放、表情切换
- API 文档：http://localhost:8000/docs
- 默认 Admin API Key：`dev-admin-key`（可在侧栏或 `.env` 修改）

## 使用流程

1. **模型管理** — 新建 Live2D 模型，上传 `.model3.json`，配置 `emotion_map`
2. **角色画像** — 创建角色，绑定模型，编写 persona prompt
3. **对话** — 在角色列表点击「对话」
4. **嵌入** — 生成 embed token，复制 iframe 代码到目标网站

### iframe 嵌入示例

```html
<iframe
  src="http://localhost:5173/embed/?token=YOUR_TOKEN"
  style="width:380px;height:600px;border:none;border-radius:12px"
></iframe>
```

## 项目结构

见 [AGENTS.md](./AGENTS.md) 与 [ARCHITECTURE.md](./ARCHITECTURE.md)。

## 测试

```bash
uv run pytest backend/tests/ -q
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | LLM API 密钥 |
| `OPENAI_BASE_URL` | OpenAI 兼容 API 地址 |
| `ADMIN_API_KEY` | 管理 API 鉴权 |
| `ASSISTANT_PORT` | 后端监听端口（默认 `8000`；若与 codeyun 等冲突可改为 `8001`） |
| `ASSISTANT_DATA_DIR` | SQLite 与音频缓存目录 |
| `CORS_ORIGINS` | 允许的前端来源 |

### 端口冲突

若本机已在跑 codeyun（默认占用 `8000` / `5173`），可在 `.env` 中设置：

```bash
ASSISTANT_PORT=8001
```

然后重新执行 `uv run dev.py`。`dev.py` 会在启动前检测端口占用并提示占用进程 PID。
