import apiClient from './client'

export async function getAnalyticsSummary() {
  const { data } = await apiClient.get('/analytics/summary')
  return data
}