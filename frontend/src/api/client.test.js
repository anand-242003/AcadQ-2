import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

describe('API client JWT interceptor', () => {
  beforeEach(() => {
    localStorage.clear()
    // Clear module cache so the interceptor re-reads localStorage fresh
    vi.resetModules()
  })

  afterEach(() => {
    localStorage.clear()
  })

  it('attaches Authorization header when token exists in localStorage', async () => {
    localStorage.setItem('acadiq_token', 'my-jwt-token')

    // Import after setting localStorage so the interceptor can read it
    const { default: api } = await import('./client.js')

    // Simulate the interceptor by running it manually on a config object
    const config = { headers: {} }
    const interceptor = api.interceptors.request.handlers[0].fulfilled
    const result = interceptor(config)

    expect(result.headers.Authorization).toBe('Bearer my-jwt-token')
  })

  it('does not attach Authorization header when no token in localStorage', async () => {
    // No token set
    const { default: api } = await import('./client.js')

    const config = { headers: {} }
    const interceptor = api.interceptors.request.handlers[0].fulfilled
    const result = interceptor(config)

    expect(result.headers.Authorization).toBeUndefined()
  })
})
