# Live2D 模型资源目录

本目录存放 `.model3.json` 及贴图等资源，由后端 `/live2d-models` 静态服务。

## 从 Open-LLM-VTuber 导入初始模型

若本机有姊妹项目 [Open-LLM-VTuber](../Open-LLM-VTuber/)，可一键创建符号链接（不复制文件）：

```bash
uv run python scripts/link_olv_models.py
```

默认链接：

| 模型 | 说明 |
|------|------|
| `mao_pro` | Mao Pro 示例，含完整表情映射 |
| `shizuku` | Shizuku 示例 |

> 模型目录使用符号链接时，后端 `StaticFiles` 需开启 `follow_symlink=True`（已默认配置）。

自定义源路径：

```bash
uv run python scripts/link_olv_models.py --source /path/to/Open-LLM-VTuber
```

链接完成后重启 `uv run dev.py`，`config/live2d_catalog.json` 中的模型会自动写入数据库，并创建示例角色「Mao 助手」「Shizuku 助手」。

也可在管理后台 **模型管理** 中手动上传或注册模型。
