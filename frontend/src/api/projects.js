import apiClient from './client'

export async function listProjects() {
  const { data } = await apiClient.get('/projects')
  return data
}

export async function createProject(payload) {
  const { data } = await apiClient.post('/projects', payload)
  return data
}

export async function deleteProject(id) {
  await apiClient.delete(`/projects/${id}`)
}