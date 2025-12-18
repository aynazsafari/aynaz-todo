import type { ApiError, Paginated, Task, TaskStatus } from './types'

const DEFAULT_BASE = 'http://localhost:8000/api/v1'
export const API_BASE = (import.meta as any).env?.VITE_API_BASE || DEFAULT_BASE

async function parseJson<T>(res: Response): Promise<T> {
  const text = await res.text()
  try { return JSON.parse(text) as T } catch { 
    // @ts-ignore
    return { detail: text } as T 
  }
}

export class HttpError extends Error {
  status: number
  body?: ApiError
  constructor(status: number, message: string, body?: ApiError) {
    super(message)
    this.status = status
    this.body = body
  }
}

export async function listTasks(params: {
  limit?: number
  offset?: number
  status?: TaskStatus | ''
  q?: string
  sort_by?: 'created_at' | 'due_at' | 'priority'
  sort_dir?: 'asc' | 'desc'
}): Promise<Paginated<Task>> {
  const url = new URL(`${API_BASE}/tasks`)
  if (params.limit != null) url.searchParams.set('limit', String(params.limit))
  if (params.offset != null) url.searchParams.set('offset', String(params.offset))
  if (params.status) url.searchParams.set('status', params.status)
  if (params.q) url.searchParams.set('q', params.q)
  if (params.sort_by) url.searchParams.set('sort_by', params.sort_by)
  if (params.sort_dir) url.searchParams.set('sort_dir', params.sort_dir)

  const res = await fetch(url, { headers: { 'Accept': 'application/json' } })
  if (!res.ok) throw await toHttpError(res)
  return parseJson<Paginated<Task>>(res)
}

export async function createTask(payload: {
  title: string
  description?: string | null
  priority?: number | null
  due_at?: string | null
}): Promise<{ data: Task }> {
  const res = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw await toHttpError(res)
  return parseJson<{ data: Task }>(res)
}

export async function updateTask(id: string, patch: {
  title?: string
  description?: string | null
  priority?: number | null
  due_at?: string | null
  status?: TaskStatus
}): Promise<{ data: Task }> {
  const res = await fetch(`${API_BASE}/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(patch),
  })
  if (!res.ok) throw await toHttpError(res)
  return parseJson<{ data: Task }>(res)
}

export async function changeStatus(id: string, status: TaskStatus): Promise<{ data: Task }> {
  const res = await fetch(`${API_BASE}/tasks/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify({ status }),
  })
  if (!res.ok) throw await toHttpError(res)
  return parseJson<{ data: Task }>(res)
}

export async function deleteTask(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/tasks/${id}`, { method: 'DELETE' })
  if (!res.ok && res.status !== 204) throw await toHttpError(res)
}

async function toHttpError(res: Response): Promise<HttpError> {
  let body: ApiError | undefined
  try { body = await parseJson<ApiError>(res) } catch {}
  const msg = body?.detail || body?.title || `HTTP ${res.status}`
  return new HttpError(res.status, msg, body)
}
