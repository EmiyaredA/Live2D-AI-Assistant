你说得对，**贴图 atlas 不是预览**，真正可用的是带 `runtime/` 目录的 **Cubism 3/4/5** 模型（含 `*.model3.json`）。

结合 [Open-LLM-VTuber](file:///Users/tonghao/Projects/Open-LLM-VTuber) 仓库和官方文档，结论如下。

---

## Open-LLM-VTuber 里实际有什么

| 项目 | 情况 |
|------|------|
| 仓库自带模型 | 仅 **2 个**：`mao_pro`、`shizuku`（见 `.gitignore` 白名单） |
| `model_dict.json` | 默认只配置了 **mao_pro** |
| 官方文档 | [Live2D 指南](https://open-llm-vtuber.github.io/docs/user-guide/live2d) 写了接入步骤，但「常见获取渠道」列表**尚未补全** |

也就是说：**OLV 不会帮你打包更多模型**，只提供接入范式；模型要自己找、自己放进 `live2d-models/`。

---

## 推荐模型来源（由易到难）

### 1. Live2D 官方免费示例（最推荐起步）

- 中文页：[Live2D 示例数据集](https://www.live2d.com/zh-CHS/learn/sample/)
- 下载入口：[sample-data](https://www.live2d.com/download/sample-data/)

下载后使用 **`runtime/` 文件夹**（内含 `model3.json`、贴图、moc3 等），不要用贴图 atlas 单图。

官方示例里较适合 VTuber / Web 的包括：

| 模型 | 特点 | 许可 |
|------|------|------|
| **虹色 Mao** (`mao_pro`) | OLV 已内置，表情/动作丰富 | 个人/小商用可，需同意许可 |
| **しずく / Shizuku** | OLV 已内置 | 同上 |
| **桃濑日和 (Hiyori)** | 经典学习向，有 PRO/FREE | 同上 |
| **马克君 (Mark)** | 结构简单，适合入门 | FREE 版 |
| **名执尽 (Natori)** | 游戏向，手腕切换 | PRO |
| **Rice** | 较完整示例 | PRO |
| **京 (Kei)** | 唇形同步示例 | PRO/FREE |
| **莲·福斯特** | Cubism 5.3 新特性 | PRO |
| **初音未来** | 联名角色 | 受 Crypton 使用条款约束 |

使用前阅读各模型 ReadMe 和 [Free Material License Agreement](https://www.live2d.jp/en/terms/live2d-free-material-license-agreement/)。

### 2. nizima 平台（官方模型商店）

- [nizima](https://nizima.com/)：Live2D 官方模型交易市场  
- [nizima LIVE](https://nizimalive.com/)：直播向模型，许可与 Cubism 示例不同，需单独看条款  

适合买正式 VTuber 用模型；下载后确认是否含 **Web/SDK 用 runtime**。

### 3. BOOTH 等创作者市场

- [BOOTH - Live2D](https://booth.pm/zh-cn/browse/live2d)  
- 大量二次元 Live2D，免费/付费都有  

注意：

- 看清是否支持 **Cubism 3+ / model3.json**
- 是否允许 **Web 嵌入 / 商用**
- 很多只给 VTube Studio 格式，需确认有 `runtime` 或可自行从 Cubism 导出

### 4. 自己制作 / 委托

- **Cubism Editor** 建模后导出「嵌入用文件一套」→ `runtime/`  
- 文档：[导出 moc3 / model3.json](https://docs.live2d.com/en/cubism-editor-manual/export-moc3-motion3-files/)

### 5. 社区 / GitHub（谨慎）

可搜 `live2d model3.json`、`pixi-live2d-display` 等，但：

- 许可不明的不建议商用  
- **不支持 Cubism 2**（`.model.json`），本项目需要 **`.model3.json`**

---

## 接入到你当前项目的步骤

与 OLV 流程一致，对应 Live2D-AI-Assistant：

```text
1. 下载模型 → 解压得到 runtime/ 目录
2. 复制到 live2d-models/<模型名>/runtime/
3. 在管理后台「模型管理」注册，或写入 config/live2d_catalog.json
4. 配置 emotion_map（对照 model3.json 里的 Expressions）
5. 在「模型预览」检查缩放与表情
```

你项目里已有：

```bash
# 链接 OLV 自带的两个模型
uv run python scripts/link_olv_models.py
```

要加官方新模型，例如桃濑日和：

```bash
# 1. 从 live2d.com 下载 Hiyori PRO，解压
# 2. 复制 runtime 到：
#    live2d-models/hiyori/runtime/hiyori.model3.json
# 3. 管理后台新建模型，model_path 填：
#    hiyori/runtime/hiyori.model3.json
```

---

## 版本与格式注意

| 要求 | 说明 |
|------|------|
| 格式 | **Cubism 3/4/5**，`*.model3.json` |
| 不支持 | Cubism 2（`.model.json`） |
| 目录 | 使用解压后的 **`runtime/`** 整包，不要只拷一张贴图 |
| 表情 | 打开 `model3.json` 看 `Expressions` 数组，再配 `emotion_map` |
| 待机 | 动作组名多为 `Idle` 或 `idle`，与 `idleMotionGroupName` 对应 |

调试工具：Live2D Cubism Viewer、VTube Studio、Live2DViewerEX。

---

## 想快速扩充模型库的建议

1. **先下 3～5 个官方免费 PRO 版**（Hiyori、Natori、Rice、Mark）——许可清晰、结构规范  
2. **再考虑 BOOTH / nizima** 买风格统一的角色  
3. **不要**从游戏解包模型用于公开产品（版权风险高）  

如果你愿意，我可以下一步帮你：

- 扩展 `scripts/link_olv_models.py`，支持从本机 Cubism 示例目录批量链接  
- 或给 `live2d_catalog.json` 预置 Hiyori / Natori 等条目模板（你下载好 runtime 后一键注册）

*当前模型：Auto（Cursor Agent Router）*