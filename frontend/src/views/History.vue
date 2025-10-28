<template>
  <div class="view-wrapper">
    <el-card class="history-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div>
            <h2>Generation History</h2>
            <p class="subtitle">Browse and manage your AI-generated images</p>
          </div>
          <el-button type="primary" @click="loadHistory">Refresh</el-button>
        </div>
      </template>

      <div v-if="loading" class="loading">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="historyItems.length">
        <el-row :gutter="24">
          <el-col v-for="item in historyItems" :key="item.id" :span="12">
            <div class="history-item">
              <div class="history-images">
                <img
                  v-for="(url, index) in item.images"
                  :key="index"
                  :src="url"
                  :alt="item.prompt"
                  @click="openPreview(item.images, index)"
                />
              </div>
              <div class="history-content">
                <div class="history-meta">
                  <el-tag size="small" :type="item.type === 'text2image' ? 'primary' : 'success'">
                    {{ item.type === 'text2image' ? 'Text → Image' : 'Image → Image' }}
                  </el-tag>
                  <span class="history-date">{{ formatDate(item.created_at) }}</span>
                </div>
                <p class="history-prompt">{{ item.prompt }}</p>
                <div class="history-actions">
                  <el-button-group>
                    <el-button type="primary" size="small" plain @click="copyPrompt(item.prompt)">
                      Copy Prompt
                    </el-button>
                    <el-button type="success" size="small" plain @click="downloadImages(item.images)">
                      Download All
                    </el-button>
                  </el-button-group>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>

        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="loadHistory"
          class="pagination"
        />
      </div>

      <el-empty v-else description="No generation history yet. Start creating some images!" />
    </el-card>

    <el-dialog
      v-model="previewVisible"
      title="Image Preview"
      :width="800"
      @close="previewVisible = false"
    >
      <el-carousel v-if="previewImages.length" :initial-index="previewIndex" indicator-position="outside">
        <el-carousel-item v-for="(url, index) in previewImages" :key="index">
          <img :src="url" alt="Preview" class="preview-image" />
        </el-carousel-item>
      </el-carousel>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { GenerationApi, type HistoryItem } from '@/api/generation'

const loading = ref(true)
const historyItems = ref<HistoryItem[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const previewVisible = ref(false)
const previewImages = ref<string[]>([])
const previewIndex = ref(0)

const loadHistory = async () => {
  loading.value = true
  try {
    const { data } = await GenerationApi.getHistory(currentPage.value, pageSize.value)
    historyItems.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('Failed to load history', error)
    ElMessage.error('Failed to load history')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

const copyPrompt = (prompt: string) => {
  navigator.clipboard.writeText(prompt)
  ElMessage.success('Prompt copied to clipboard')
}

const downloadImages = (images: string[]) => {
  images.forEach((url, index) => {
    fetch(url)
      .then((response) => response.blob())
      .then((blob) => {
        const a = document.createElement('a')
        a.href = window.URL.createObjectURL(blob)
        a.download = `generated-${index + 1}.png`
        a.click()
        window.URL.revokeObjectURL(a.href)
      })
      .catch((error) => {
        console.error('Download failed', error)
        ElMessage.error('Failed to download image')
      })
  })
}

const openPreview = (images: string[], index: number) => {
  previewImages.value = images
  previewIndex.value = index
  previewVisible.value = true
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped lang="scss">
.view-wrapper {
  padding: 1rem 0;
}

.history-card {
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

.loading {
  padding: 2rem;
}

.history-item {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  transition: all 0.3s;

  &:hover {
    border-color: rgba(59, 130, 246, 0.5);
    transform: translateY(-2px);
  }
}

.history-images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.5rem;
  padding: 1rem;

  img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    border-radius: 12px;
    cursor: pointer;
    transition: transform 0.3s;

    &:hover {
      transform: scale(1.05);
    }
  }
}

.history-content {
  padding: 1rem;
}

.history-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.history-date {
  font-size: 0.85rem;
  color: rgba(148, 163, 184, 0.9);
}

.history-prompt {
  margin: 0 0 1rem 0;
  color: rgba(226, 232, 240, 0.9);
  line-height: 1.6;
}

.history-actions {
  display: flex;
  justify-content: flex-end;
}

.pagination {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

.preview-image {
  width: 100%;
  height: auto;
  display: block;
}
</style>
