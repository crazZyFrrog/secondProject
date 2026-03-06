const API_BASE_URL = '/api'

type RequestOptions = {
  method?: string
  body?: unknown
  token?: string | null
}

export function getAuthToken() {
  return localStorage.getItem('token')
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, token } = options
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  })

  const contentType = response.headers.get('content-type') || ''
  let data: any = null
  if (contentType.includes('application/json')) {
    data = await response.json()
  } else {
    const text = await response.text()
    data = text ? { message: text } : null
  }

  if (!response.ok) {
    const message =
      data?.message ||
      data?.detail?.message ||
      `Request failed with status ${response.status}`
    const error = new Error(message)
    const fieldErrors = data?.fieldErrors || data?.detail?.fieldErrors
    if (fieldErrors) {
      ;(error as Error & { fieldErrors?: Record<string, string> }).fieldErrors = fieldErrors
    }
    throw error
  }

  return data as T
}
