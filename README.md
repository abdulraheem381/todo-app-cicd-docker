# Simple Python & Node.js Todo App

This project consists of a Python Flask backend and a Node.js (React) frontend.

## Prerequisites

- Python 3.x
- Node.js & npm

## Structure

- `/backend`: Python Flask API with SQLite database.
- `/frontend`: React frontend using Vite.

## Setup & Run

### Backend

1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```
   The backend runs on `http://localhost:5000`.

### Frontend

1. Navigate to `frontend/`:
   ```bash
   cd frontend
   ```
2. Install dependencies (if not already done):
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend runs on `http://localhost:5173`.

## Features

- Create, Read, Update, Delete (CRUD) Todos.
- Data persisted in SQLite (`backend/todo.db`).
- Modern dark/light mode React UI.

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs automatically on push/PR to `main`.

### Current Stages:
1. **Details**:
   - Backend: Lints with `flake8` and tests with `pytest`.
   - Frontend: Lints with `eslint` and tests with `vitest`.

### Deployment:
The **Docker Build & Push** step has been intentionally removed from the initial pipeline. This step is reserved for manual configuration or future implementation as per project requirements.
