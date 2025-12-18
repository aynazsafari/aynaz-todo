export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE'

export type Task = {
  id: string
  title: string
  description: string | null
  status: TaskStatus
  priority: number | null
  due_at: string | null
  created_at: string
  updated_at: string
}

export type Paginated<T> = {
  data: T[]
  meta?: {
    pagination?: {
      limit: number
      offset: number
      total: number
    }
  }
}

export type ApiError = {
  type?: string
  title?: string
  status?: number
  detail?: string
  trace_id?: string
  errors?: { field?: string; message?: string }[]
}
