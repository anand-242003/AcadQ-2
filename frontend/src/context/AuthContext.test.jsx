import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, act } from '@testing-library/react'
import { AuthProvider, useAuth } from './AuthContext'

// Helper component to expose context values
function TestConsumer() {
  const { user, token, isAuthenticated, login, logout } = useAuth()
  return (
    <div>
      <span data-testid="is-auth">{String(isAuthenticated)}</span>
      <span data-testid="user-name">{user?.name || 'null'}</span>
      <span data-testid="token">{token || 'null'}</span>
      <button onClick={() => login('test-token', { name: 'Alice', email: 'alice@test.com' })}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  )
}

describe('AuthContext', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('starts unauthenticated when no localStorage data', () => {
    render(<AuthProvider><TestConsumer /></AuthProvider>)
    expect(screen.getByTestId('is-auth').textContent).toBe('false')
    expect(screen.getByTestId('token').textContent).toBe('null')
  })

  it('login persists token and user to localStorage', () => {
    render(<AuthProvider><TestConsumer /></AuthProvider>)
    act(() => { screen.getByText('Login').click() })
    expect(localStorage.getItem('acadiq_token')).toBe('test-token')
    expect(JSON.parse(localStorage.getItem('acadiq_user')).name).toBe('Alice')
  })

  it('login sets isAuthenticated to true', () => {
    render(<AuthProvider><TestConsumer /></AuthProvider>)
    act(() => { screen.getByText('Login').click() })
    expect(screen.getByTestId('is-auth').textContent).toBe('true')
  })

  it('logout clears localStorage and resets state', () => {
    localStorage.setItem('acadiq_token', 'existing-token')
    localStorage.setItem('acadiq_user', JSON.stringify({ name: 'Bob', email: 'bob@test.com' }))
    render(<AuthProvider><TestConsumer /></AuthProvider>)
    act(() => { screen.getByText('Logout').click() })
    expect(localStorage.getItem('acadiq_token')).toBeNull()
    expect(screen.getByTestId('is-auth').textContent).toBe('false')
  })

  it('initializes from localStorage on mount', () => {
    localStorage.setItem('acadiq_token', 'stored-token')
    localStorage.setItem('acadiq_user', JSON.stringify({ name: 'Carol', email: 'carol@test.com' }))
    render(<AuthProvider><TestConsumer /></AuthProvider>)
    expect(screen.getByTestId('is-auth').textContent).toBe('true')
    expect(screen.getByTestId('user-name').textContent).toBe('Carol')
  })
})
