import apiClient from './client'

export async function createSmartTask(text) {
  const { data } = await apiClient.post('/ai/smart-task', { text })
  return data
}