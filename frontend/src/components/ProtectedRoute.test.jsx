import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'

// Mock AuthContext
vi.mock('../context/AuthContext', () => ({
  useAuth: vi.fn(),
}))

import { useAuth } from '../context/AuthContext'

describe('ProtectedRoute', () => {
  it('renders children when authenticated', () => {
    useAuth.mockReturnValue({ isAuthenticated: true })
    render(
      <MemoryRouter>
        <ProtectedRoute><div>Protected Content</div></ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.getByText('Protected Content')).toBeTruthy()
  })

  it('redirects to /auth when not authenticated', () => {
    useAuth.mockReturnValue({ isAuthenticated: false })
    render(
      <MemoryRouter initialEntries={['/input']}>
        <ProtectedRoute><div>Protected Content</div></ProtectedRoute>
      </MemoryRouter>
    )
    expect(screen.queryByText('Protected Content')).toBeNull()
  })
})
