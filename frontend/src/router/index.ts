import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/text2image',
    name: 'Text2Image',
    component: () => import('@/views/Text2Image.vue'),
  },
  {
    path: '/image2image',
    name: 'Image2Image',
    component: () => import('@/views/Image2Image.vue'),
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
