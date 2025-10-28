<template>
  <div class="home-wrapper">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">AI Image Generation</h1>
        <p class="hero-subtitle">
          Create stunning images from text descriptions or transform existing images with advanced AI technology
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/text2image')">
            Get Started
          </el-button>
          <el-button size="large" @click="$router.push('/history')">View History</el-button>
        </div>
      </div>
    </div>

    <el-row :gutter="24" class="features">
      <el-col :span="8">
        <el-card shadow="hover" class="feature-card">
          <div class="feature-icon">🖼️</div>
          <h3>Text to Image</h3>
          <p>Generate images from text descriptions using state-of-the-art AI models</p>
          <el-button type="primary" text @click="$router.push('/text2image')">Try Now →</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="feature-card">
          <div class="feature-icon">🎨</div>
          <h3>Image to Image</h3>
          <p>Transform your images with AI-powered style transfer and modifications</p>
          <el-button type="primary" text @click="$router.push('/image2image')">Try Now →</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="feature-card">
          <div class="feature-icon">📚</div>
          <h3>History</h3>
          <p>Browse and manage all your generated images in one place</p>
          <el-button type="primary" text @click="$router.push('/history')">View History →</el-button>
        </el-card>
      </el-col>
    </el-row>

    <div class="stats-section">
      <el-row :gutter="24">
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-value">{{ healthInfo.status }}</div>
            <div class="stat-label">Service Status</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-value">v{{ healthInfo.version }}</div>
            <div class="stat-label">Version</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-value">{{ healthInfo.volcengine_configured ? 'Yes' : 'Demo' }}</div>
            <div class="stat-label">API Configured</div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const healthInfo = ref({
  status: 'Loading...',
  version: '1.0.0',
  volcengine_configured: false,
})

onMounted(async () => {
  try {
    const { data } = await axios.get('/health')
    healthInfo.value = data
  } catch (error) {
    console.error('Failed to fetch health info', error)
  }
})
</script>

<style scoped lang="scss">
.home-wrapper {
  padding: 2rem 0;
}

.hero-section {
  padding: 4rem 0;
  text-align: center;
  margin-bottom: 4rem;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(148, 163, 184, 0.9);
  margin: 0 0 2rem 0;
  line-height: 1.8;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.features {
  margin-bottom: 4rem;
}

.feature-card {
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 18px;
  text-align: center;
  padding: 2rem 1rem;
  transition: all 0.3s;
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
    border-color: rgba(59, 130, 246, 0.5);
  }
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin: 0 0 1rem 0;
}

.feature-card p {
  color: rgba(148, 163, 184, 0.9);
  margin: 0 0 1rem 0;
}

.stats-section {
  margin-top: 4rem;
}

.stat-card {
  background: rgba(30, 41, 59, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 18px;
  padding: 2rem;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.95rem;
  color: rgba(148, 163, 184, 0.9);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
