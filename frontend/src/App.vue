<template>
  <div id="app" class="app-container">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <span class="logo-icon">🎨</span>
            <span class="logo-text">Volcengine Image Generator</span>
          </div>
          <el-menu
            mode="horizontal"
            :default-active="activeIndex"
            router
            class="nav-menu"
            background-color="#1f2937"
            text-color="#e5e7eb"
            active-text-color="#3b82f6"
          >
            <el-menu-item index="/">Home</el-menu-item>
            <el-menu-item index="/text2image">Text to Image</el-menu-item>
            <el-menu-item index="/image2image">Image to Image</el-menu-item>
            <el-menu-item index="/history">History</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeIndex = ref(route.path)

watch(
  () => route.path,
  (newPath) => {
    activeIndex.value = newPath
  }
)
</script>

<style scoped lang="scss">
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

.app-header {
  background: #1f2937;
  border-bottom: 1px solid #374151;
  padding: 0;
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #f9fafb;
}

.logo-icon {
  font-size: 1.75rem;
}

.nav-menu {
  border: none;
}

.app-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

:deep(.el-menu--horizontal .el-menu-item) {
  border-bottom: none;
}

:deep(.el-menu--horizontal .el-menu-item:hover) {
  background-color: #374151;
}
</style>
