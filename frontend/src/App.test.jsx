import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import App from './App'

// Mock axios
vi.mock('axios')

describe('App', () => {
    it('renders Todo List title', () => {
        render(<App />)
        expect(screen.getByText('Task Master')).toBeInTheDocument()
    })

    it('renders input field', () => {
        render(<App />)
        const inputElement = screen.getByPlaceholderText(/Add a new task/i)
        expect(inputElement).toBeInTheDocument()
    })
    // Add more tests as needed
})
