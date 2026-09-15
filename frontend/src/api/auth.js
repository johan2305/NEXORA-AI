import apiClient from './client'

export async function register({ email, password, fullName, organizationName }) {
  const { data } = await apiClient.post('/auth/register', {
    email,
    password,
    full_name: fullName,
    organization_name: organizationName,
  })
  return data
}

export async function login({ email, password }) {
  const { data } = await apiClient.post('/auth/login', { email, password })
  return data
}

export function saveTokens({ access_token, refresh_token }) {
  localStorage.setItem('nexora-access-token', access_token)
  localStorage.setItem('nexora-refresh-token', refresh_token)
}

export function clearTokens() {
  localStorage.removeItem('nexora-access-token')
  localStorage.removeItem('nexora-refresh-token')
}

export function isAuthenticated() {
  return !!localStorage.getItem('nexora-access-token')
}