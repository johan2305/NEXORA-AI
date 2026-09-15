import apiClient from './client'

export async function listNotifications() {
  const { data } = await apiClient.get('/notifications')
  return data
}

export async function markNotificationAsRead(id) {
  await apiClient.post(`/notifications/${id}/read`)
}