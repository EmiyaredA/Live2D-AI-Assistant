<template>
  <div class="characters-page">
    <div class="page-header">
      <h2>角色画像</h2>
      <el-button type="primary" @click="openCreate">新建角色</el-button>
    </div>

    <el-table :data="characters" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="live2d_model_id" label="模型 ID" width="100" />
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="primary" @click="goChat(row.id)">对话</el-button>
          <el-button size="small" type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑角色' : '新建角色'" width="640px">
      <el-form label-width="110px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="Live2D 模型">
          <div class="characters-page__model-row">
            <el-select
              v-model="form.live2d_model_id"
              clearable
              placeholder="选择模型"
              style="flex: 1"
            >
              <el-option
                v-for="m in modelOptions"
                :key="m.id"
                :label="`${m.name} (#${m.id})`"
                :value="m.id"
              />
            </el-select>
            <el-button
              :disabled="!form.live2d_model_id"
              @click="previewSelectedModel"
            >
              预览模型
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="人设 Prompt">
          <el-input v-model="form.persona_prompt" type="textarea" :rows="8" />
        </el-form-item>
        <el-form-item label="LLM 模型">
          <el-input v-model="form.llm_model" placeholder="gpt-4o-mini" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  createCharacter,
  deleteCharacter,
  listCharacters,
  updateCharacter,
  type Character,
} from '@/api/characters'
import { listLive2DModels, type Live2DModel } from '@/api/live2dModels'

const router = useRouter()
const characters = ref<Character[]>([])
const modelOptions = ref<Live2DModel[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<Character | null>(null)
const form = reactive({
  name: '',
  persona_prompt: '你是一位活泼可爱的二次元 AI 助手。',
  live2d_model_id: null as number | null,
  llm_model: 'gpt-4o-mini',
})

async function load() {
  loading.value = true
  try {
    ;[characters.value, modelOptions.value] = await Promise.all([
      listCharacters(),
      listLive2DModels(),
    ])
  } catch {
    ElMessage.error('加载失败，请检查 Admin API Key')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  form.name = ''
  form.persona_prompt = '你是一位活泼可爱的二次元 AI 助手。'
  form.live2d_model_id = null
  form.llm_model = 'gpt-4o-mini'
  dialogVisible.value = true
}

function openEdit(row: Character) {
  editing.value = row
  form.name = row.name
  form.persona_prompt = row.persona_prompt
  form.live2d_model_id = row.live2d_model_id
  form.llm_model = (row.llm_config?.model as string) || 'gpt-4o-mini'
  dialogVisible.value = true
}

async function save() {
  const body = {
    name: form.name,
    persona_prompt: form.persona_prompt,
    live2d_model_id: form.live2d_model_id,
    llm_config: { engine: 'basic_memory', model: form.llm_model },
  }
  try {
    if (editing.value) {
      await updateCharacter(editing.value.id, body)
    } else {
      await createCharacter(body)
    }
    dialogVisible.value = false
    await load()
    ElMessage.success('已保存')
  } catch {
    ElMessage.error('保存失败')
  }
}

async function remove(id: number) {
  await deleteCharacter(id)
  await load()
}

function goChat(id: number) {
  router.push(`/chat/${id}`)
}

function previewSelectedModel() {
  if (!form.live2d_model_id) return
  router.push({ name: 'AdminPreviewModel', params: { modelId: String(form.live2d_model_id) } })
}

onMounted(async () => {
  await load()
  const previewModelId = router.currentRoute.value.query.previewModelId
  if (previewModelId) {
    form.live2d_model_id = Number(previewModelId)
    openCreate()
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.characters-page__model-row {
  display: flex;
  gap: 8px;
  width: 100%;
}
</style>
