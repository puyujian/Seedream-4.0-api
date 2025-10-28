import apiClient from './client'

export interface Text2ImagePayload {
  prompt: string
  negative_prompt?: string
  width: number
  height: number
  steps: number
  scale: number
  seed?: number | null
  style_preset: string
  num_images: number
}

export interface Image2ImagePayload extends Omit<Text2ImagePayload, 'num_images' | 'width' | 'height'> {
  image: string
  strength: number
}

export interface TaskResponse {
  task_id: string
  status: string
  message: string
  created_at: string
}

export interface TaskStatusResponse {
  task_id: string
  status: string
  progress?: number
  images?: string[]
  error?: string
  created_at: string
  completed_at?: string | null
}

export interface HistoryItem {
  id: string
  task_id: string
  type: string
  prompt: string
  negative_prompt?: string
  parameters: Record<string, unknown>
  images: string[]
  created_at: string
  favorite: boolean
}

export interface HistoryResponse {
  total: number
  items: HistoryItem[]
  page: number
  page_size: number
}

export const GenerationApi = {
  textToImage(payload: Text2ImagePayload) {
    return apiClient.post<TaskResponse>('/generate/text2image', payload)
  },

  imageToImage(payload: Image2ImagePayload) {
    return apiClient.post<TaskResponse>('/generate/image2image', payload)
  },

  getTaskStatus(taskId: string) {
    return apiClient.get<TaskStatusResponse>(`/tasks/${taskId}`)
  },

  listTasks() {
    return apiClient.get<TaskStatusResponse[]>('/tasks/')
  },

  getHistory(page = 1, pageSize = 20) {
    return apiClient.get<HistoryResponse>('/tasks/history', {
      params: { page, page_size: pageSize },
    })
  },
}
