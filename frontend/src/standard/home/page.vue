<template>
  <div class="home-page">
    <el-card shadow="never" class="hero-card">
      <h1>Live2D AI 助手平台</h1>
      <p>创建角色、上传 Live2D 模型、生成嵌入代码，将二次元助手带到你的网站。</p>
      <div class="hero-actions">
        <el-button type="primary" @click="$router.push('/admin/characters')">创建角色</el-button>
        <el-button @click="$router.push('/admin/models')">管理模型</el-button>
        <el-button @click="$router.push('/admin/preview')">模型预览</el-button>
        <el-button @click="$router.push('/admin/embed')">嵌入代码</el-button>
      </div>
    </el-card>

    <el-row :gutter="16" class="feature-row">
      <el-col :span="8">
        <el-card shadow="hover">
          <h3>网站助手</h3>
          <p>全屏对话页 + iframe 嵌入，WebSocket 实时对话与 TTS。</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <h3>可扩展模型</h3>
          <p>上传 .model3.json，配置 emotionMap 与角色人设。</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <h3>Agent 扩展</h3>
          <p>预留 MCP / Skill 配置，桌宠模式 Phase 2 接入。</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.hero-card {
  margin-bottom: 20px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.feature-row h3 {
  margin-top: 0;
}

.feature-row p {
  color: #606266;
}
</style>
