# Aynaz To-Do (Pinterest-style Frontend)

This folder is a Vite + React frontend designed to **look like the Pinterest dashboard screenshot**:
- pastel mint background
- left icon sidebar
- big headline + chips
- card grid
- right profile panel

It still supports your university CRUD requirements by calling these endpoints:
- GET /api/v1/tasks (filters/search/pagination)
- POST /api/v1/tasks
- PATCH /api/v1/tasks/{id}
- PATCH /api/v1/tasks/{id}/status
- DELETE /api/v1/tasks/{id}

## Run on Windows (PowerShell)
1) cd into this `frontend` folder
2) `npm install`
3) `npm run dev`
Open: http://localhost:5173

Backend base URL defaults to http://localhost:8000/api/v1
You can override by creating `.env` based on `.env.example`.
