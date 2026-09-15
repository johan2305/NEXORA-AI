import apiClient from './client'

export async function listAutomations() {
  const { data } = await apiClient.get('/automations')
  return data
}

export async function createAutomation(payload) {
  const { data } = await apiClient.post('/automations', payload)
  return data
}

export async function deleteAutomation(id) {
  await apiClient.delete(`/automations/${id}`)
}

export async function runAutomation(id) {
  const { data } = await apiClient.post(`/automations/${id}/run`)
  return data
}

export async function listExecutions(id) {
  const { data } = await apiClient.get(`/automations/${id}/executions`)
  return data
}