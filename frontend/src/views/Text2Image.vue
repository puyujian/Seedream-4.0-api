<template>
  <div class="view-wrapper">
    <el-card class="form-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div>
            <h2>Text to Image</h2>
            <p class="subtitle">Transform your imagination into stunning visuals with AI.</p>
          </div>
          <el-button type="primary" @click="resetForm" :disabled="isSubmitting">Reset</el-button>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="140px" class="form-layout">
        <el-form-item label="Prompt" prop="prompt">
          <el-input
            v-model="form.prompt"
            type="textarea"
            :rows="4"
            placeholder="Describe the image you want to create"
          />
        </el-form-item>

        <el-form-item label="Negative Prompt">
          <el-input
            v-model="form.negative_prompt"
            type="textarea"
            :rows="3"
            placeholder="Describe what you DON'T want to see"
          />
        </el-form-item>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="Width" prop="width">
              <el-input-number v-model="form.width" :min="64" :max="2048" :step="64" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Height" prop="height">
              <el-input-number v-model="form.height" :min="64" :max="2048" :step="64" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="Steps" prop="steps">
              <el-slider v-model="form.steps" :min="10" :max="100" :step="1" show-input />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="CFG Scale" prop="scale">
              <el-slider v-model="form.scale" :min="1" :max="20" :step="0.5" show-input />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="Seed">
              <el-input-number v-model="form.seed" :step="1" :min="-1" :max="999999" />
              <span class="input-hint">-1 for random seed</span>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Number of Images" prop="num_images">
              <el-input-number v-model="form.num_images" :min="1" :max="4" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="Style Preset">
          <el-select v-model="form.style_preset" placeholder="Select a style">
            <el-option label="None" value="none" />
            <el-option label="Anime" value="anime" />
            <el-option label="Photographic" value="photographic" />
            <el-option label="Digital Art" value="digital_art" />
            <el-option label="Comic Book" value="comic_book" />
            <el-option label="Fantasy Art" value="fantasy_art" />
            <el-option label="Cinematic" value="cinematic" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" :loading="isSubmitting" @click="handleSubmit">
            {{ isSubmitting ? 'Generating...' : 'Generate Image' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="results.length" class="result-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div>
            <h2>Results</h2>
            <p class="subtitle">Your generated images will appear below</p>
          </div>
          <el-tag type="success" v-if="currentStatus === 'completed'">Completed</el-tag>
          <el-tag type="warning" v-else-if="currentStatus === 'processing'">Processing...</el-tag>
          <el-tag type="info" v-else-if="currentStatus === 'pending'">Queued</el-tag>
        </div>
      </template>

      <el-row :gutter="24">
        <el-col v-for="(url, index) in results" :key="index" :span="12">
          <div class="image-card">
            <img :src="url" :alt="`Generated image ${index + 1}`" />
            <div class="image-actions">
              <el-button-group>
                <el-button type="primary" plain @click="openInNewTab(url)">Open</el-button>
                <el-button type="success" plain @click="downloadImage(url, `generated-${index + 1}.png`)">Download</el-button>
              </el-button-group>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-empty v-else description="Generated images will appear here" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElForm, ElMessage } from 'element-plus'
import { GenerationApi, type Text2ImagePayload, type TaskStatusResponse } from '@/api/generation'

interface FormModel extends Text2ImagePayload {}

const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const isSubmitting = ref(false)
const currentTaskId = ref<string | null>(null)
const currentStatus = ref<string>('')
const results = ref<string[]>([])

const form = reactive<FormModel>({
  prompt: '',
  negative_prompt: '',
  width: 512,
  height: 512,
  steps: 30,
  scale: 7.5,
  seed: -1,
  style_preset: 'none',
  num_images: 1,
})

const rules = {
  prompt: [
    { required: true, message: 'Prompt is required', trigger: 'blur' },
    { min: 5, message: 'Prompt should be more descriptive', trigger: 'blur' },
  ],
  width: [{ required: true, message: 'Width is required', trigger: 'change' }],
  height: [{ required: true, message: 'Height is required', trigger: 'change' }],
  steps: [{ required: true, message: 'Steps are required', trigger: 'change' }],
  scale: [{ required: true, message: 'Scale is required', trigger: 'change' }],
  num_images: [{ required: true, message: 'Please select number of images', trigger: 'change' }],
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('Please fix the form errors before submitting')
      return
    }

    try {
      isSubmitting.value = true
      results.value = []
      currentStatus.value = 'pending'

      const payload: Text2ImagePayload = {
        prompt: form.prompt,
        negative_prompt: form.negative_prompt || undefined,
        width: form.width,
        height: form.height,
        steps: form.steps,
        scale: form.scale,
        seed: form.seed === -1 ? undefined : form.seed,
        style_preset: form.style_preset,
        num_images: form.num_images,
      }

      const { data } = await GenerationApi.textToImage(payload)
      currentTaskId.value = data.task_id
      ElMessage.success('Task submitted! Generating images...')

      pollTaskStatus(data.task_id)
    } catch (error: any) {
      console.error('Generation failed', error)
      ElMessage.error(error?.response?.data?.detail || 'Failed to submit generation task')
    } finally {
      isSubmitting.value = false
    }
  })
}

const pollTaskStatus = async (taskId: string) => {
  const checkStatus = async () => {
    try {
      const { data } = await GenerationApi.getTaskStatus(taskId)
      currentStatus.value = data.status

      if (data.status === 'completed' && data.images?.length) {
        results.value = data.images
        ElMessage.success('Image generation completed!')
        return true
      }

      if (data.status === 'failed') {
        ElMessage.error(data.error || 'Generation failed')
        return true
      }

      return false
    } catch (error) {
      console.error('Failed to fetch task status', error)
      ElMessage.error('Unable to fetch task status')
      return true
    }
  }

  const interval = setInterval(async () => {
    const shouldStop = await checkStatus()
    if (shouldStop) {
      clearInterval(interval)
    }
  }, 2000)
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
  form.prompt = ''
  form.negative_prompt = ''
  form.width = 512
  form.height = 512
  form.steps = 30
  form.scale = 7.5
  form.seed = -1
  form.style_preset = 'none'
  form.num_images = 1
  results.value = []
  currentTaskId.value = null
  currentStatus.value = ''
}

const openInNewTab = (url: string) => {
  window.open(url, '_blank')
}

const downloadImage = async (url: string, filename: string) => {
  try {
    const response = await fetch(url)
    const blob = await response.blob()

    const a = document.createElement('a')
    a.href = window.URL.createObjectURL(blob)
    a.download = filename
    a.click()
    window.URL.revokeObjectURL(a.href)
  } catch (error) {
    console.error('Download failed', error)
    ElMessage.error('Failed to download image')
  }
}
</script>

<style scoped lang="scss">
.view-wrapper {
  display: grid;
  gap: 2rem;
}

.form-card,
.result-card {
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 18px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subtitle {
  margin: 0;
  color: rgba(148, 163, 184, 0.9);
}

.form-layout {
  padding: 1rem 0;
}

.input-hint {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: rgba(148, 163, 184, 0.9);
}

.image-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.35);
}

.image-card img {
  width: 100%;
  display: block;
}

.image-actions {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>
