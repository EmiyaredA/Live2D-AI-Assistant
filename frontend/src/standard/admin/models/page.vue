<template>
  <div class="models-page">
    <div class="page-header">
      <h2>Live2D 模型管理</h2>
      <el-button type="primary" @click="openCreate">新建模型</el-button>
    </div>

    <el-table :data="models" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="model_path" label="模型路径" />
      <el-table-column label="操作" width="340">
        <template #default="{ row }">
          <el-button size="small" type="primary" @click="openPreviewPage(row)">预览</el-button>
          <el-upload
            :show-file-list="false"
            :http-request="(opt: { file: File }) => handleUpload(row.id, opt)"
            style="display: inline-block; margin-right: 8px"
          >
            <el-button size="small">上传</el-button>
          </el-upload>
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑模型' : '新建模型'" width="520px">
      <el-form label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="模型路径">
          <el-input v-model="form.model_path" placeholder="如 mao_pro/mao_pro.model3.json" />
        </el-form-item>
        <el-form-item label="表情映射">
          <el-input
            v-model="emotionMapText"
            type="textarea"
            :rows="5"
            placeholder='{"joy": 0, "sad": 1}'
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button v-if="editing" @click="openPreview(editing)">预览</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="previewVisible" :title="`预览：${previewModel?.name || ''}`" width="920px" top="4vh">
      <ModelPreviewPanel
        v-if="previewModel"
        :model-info="previewModelInfo"
        :model-path="previewModel.model_path"
      >
        <template #actions>
          <el-button type="primary" link @click="openPreviewPage(previewModel!)">
            在全屏预览页打开
          </el-button>
        </template>
      </ModelPreviewPanel>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  createLive2DModel,
  deleteLive2DModel,
  listLive2DModels,
  updateLive2DModel,
  uploadModelFile,
  type Live2DModel,
} from '@/api/live2dModels'
import ModelPreviewPanel from '@/components/ModelPreviewPanel.vue'
import { toModelInfo } from '@/utils/live2dModel'

const router = useRouter()
const models = ref<Live2DModel[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const previewVisible = ref(false)
const previewModel = ref<Live2DModel | null>(null)
const editing = ref<Live2DModel | null>(null)
const emotionMapText = ref('{"joy": 0, "neutral": 1}')
const form = reactive({ name: '', model_path: '' })

const previewModelInfo = computed(() =>
  previewModel.value ? toModelInfo(previewModel.value) : null,
)

function openPreview(row: Live2DModel) {
  previewModel.value = row
  previewVisible.value = true
}

function openPreviewPage(row: Live2DModel) {
  router.push({ name: 'AdminPreviewModel', params: { modelId: String(row.id) } })
}

async function load() {
  loading.value = true
  try {
    models.value = await listLive2DModels()
  } catch {
    ElMessage.error('加载模型失败，请检查 Admin API Key')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.name = ''
  form.model_path = ''
  emotionMapText.value = '{"joy": 0, "neutral": 1}'
  dialogVisible.value = true
}

function openEdit(row: Live2DModel) {
  editing.value = row
  form.name = row.name
  form.model_path = row.model_path
  emotionMapText.value = JSON.stringify(row.emotion_map || {}, null, 2)
  dialogVisible.value = true
}

async function save() {
  let emotion_map = {}
  try {
    emotion_map = JSON.parse(emotionMapText.value || '{}')
  } catch {
    ElMessage.error('表情映射 JSON 格式错误')
    return
  }

  try {
    if (editing.value) {
      await updateLive2DModel(editing.value.id, {
        name: form.name,
        model_path: form.model_path,
        emotion_map,
      })
    } else {
      await createLive2DModel({
        name: form.name,
        model_path: form.model_path,
        emotion_map,
      })
    }
    dialogVisible.value = false
    await load()
    ElMessage.success('已保存')
  } catch {
    ElMessage.error('保存失败')
  }
}

async function remove(id: number) {
  await deleteLive2DModel(id)
  await load()
}

async function handleUpload(id: number, opt: { file: File }) {
  try {
    await uploadModelFile(id, opt.file)
    ElMessage.success('上传成功')
    await load()
  } catch {
    ElMessage.error('上传失败')
  }
}

onMounted(load)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
</style>
