import React, { useEffect, useMemo, useState } from 'react'
import Sidebar from './components/Sidebar'
import ChipBar from './components/ChipBar'
import TaskCard from './components/TaskCard'
import TaskModal from './components/TaskModal'
import Pagination from './components/Pagination'
import type { Task, TaskStatus } from './types'
import { API_BASE, changeStatus, createTask, deleteTask, listTasks, updateTask, HttpError } from './api'
import { Search, Sparkles, Bell, SlidersHorizontal } from 'lucide-react'

const CHIPS = [
  { key: 'all', label: 'All' },
  { key: 'TODO', label: 'To do' },
  { key: 'IN_PROGRESS', label: 'In progress' },
  { key: 'DONE', label: 'Done' },
] as const

function nextStatus(s: TaskStatus): TaskStatus {
  if (s === 'TODO') return 'IN_PROGRESS'
  if (s === 'IN_PROGRESS') return 'DONE'
  return 'TODO'
}

export default function App() {
  const [activeNav, setActiveNav] = useState('home')
  const [chip, setChip] = useState<typeof CHIPS[number]['key']>('all')
  const [q, setQ] = useState('')
  const [sortBy, setSortBy] = useState<'created_at' | 'due_at' | 'priority'>('created_at')
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc')

  const [limit, setLimit] = useState(6)
  const [offset, setOffset] = useState(0)

  const [tasks, setTasks] = useState<Task[]>([])
  const [total, setTotal] = useState(0)

  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [modalOpen, setModalOpen] = useState(false)
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create')
  const [editing, setEditing] = useState<Task | null>(null)

  const statusFilter: TaskStatus | '' = useMemo(() => {
    if (chip === 'all') return ''
    return chip as TaskStatus
  }, [chip])

  const counts = useMemo(() => {
    const c = { TODO: 0, IN_PROGRESS: 0, DONE: 0 }
    for (const t of tasks) c[t.status]++
    return c
  }, [tasks])

  async function refresh(resetOffset = false) {
    try {
      setBusy(true)
      setError(null)
      const res = await listTasks({
        limit,
        offset: resetOffset ? 0 : offset,
        status: statusFilter,
        q,
        sort_by: sortBy,
        sort_dir: sortDir,
      })
      setTasks(res.data || [])
      setTotal(res.meta?.pagination?.total ?? (res.data?.length ?? 0))
      if (resetOffset) setOffset(0)
    } catch (e) {
      const msg =
        e instanceof HttpError
          ? `${e.message}${e.body?.trace_id ? ` (trace: ${e.body.trace_id})` : ''}`
          : 'Failed to fetch from API.'
      setError(msg)
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => { refresh(true) }, [chip, sortBy, sortDir, limit])
  useEffect(() => { refresh(false) }, [offset])

  function openCreate() {
    setModalMode('create')
    setEditing(null)
    setModalOpen(true)
  }

  function openEdit(t: Task) {
    setModalMode('edit')
    setEditing(t)
    setModalOpen(true)
  }

  async function onSubmit(payload: { title: string; description: string | null; priority: number | null; due_at: string | null }) {
    try {
      setBusy(true)
      setError(null)
      if (modalMode === 'create') {
        await createTask(payload)
      } else if (editing) {
        await updateTask(editing.id, payload)
      }
      setModalOpen(false)
      await refresh(true)
    } catch (e) {
      const msg = e instanceof HttpError ? e.message : 'Request failed.'
      setError(msg)
    } finally {
      setBusy(false)
    }
  }

  async function onDelete(id: string) {
    if (!confirm('Delete this task?')) return
    try {
      setBusy(true)
      setError(null)
      await deleteTask(id)
      await refresh(true)
    } catch (e) {
      setError(e instanceof HttpError ? e.message : 'Delete failed.')
    } finally {
      setBusy(false)
    }
  }

  async function onToggleStatus(t: Task) {
    try {
      setBusy(true)
      setError(null)
      await changeStatus(t.id, nextStatus(t.status))
      await refresh(false)
    } catch (e) {
      setError(e instanceof HttpError ? e.message : 'Status change failed.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="app">
      <Sidebar active={activeNav} onActive={setActiveNav} />

      <main className="main">
        <header className="top">
          <div className="top__left">
            <div className="headline">
              <div className="headline__kicker"><Sparkles size={16} /> Aynaz To-Do</div>
              <h1>Invest in your productivity</h1>
              <p>CRUD-ready To-Do dashboard connected to your backend API.</p>
            </div>

            <div className="searchRow">
              <div className="search">
                <Search size={16} />
                <input
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  placeholder="Search tasks by title..."
                  onKeyDown={(e) => { if (e.key === 'Enter') refresh(true) }}
                />
              </div>

              <button className="btnSoft" onClick={() => refresh(true)} type="button" title="Apply search">
                Apply
              </button>

              <button className="btnPrimary" onClick={openCreate} type="button">
                + New task
              </button>
            </div>

            <div className="chipRow">
              <ChipBar
                chips={CHIPS.map(c => ({ key: c.key, label: c.label }))}
                active={chip}
                onChange={(k) => { setChip(k as any); }}
              />

              <div className="sort">
                <SlidersHorizontal size={16} />
                <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)}>
                  <option value="created_at">Created</option>
                  <option value="due_at">Due date</option>
                  <option value="priority">Priority</option>
                </select>
                <select value={sortDir} onChange={(e) => setSortDir(e.target.value as any)}>
                  <option value="desc">Desc</option>
                  <option value="asc">Asc</option>
                </select>

                <select value={limit} onChange={(e) => { setLimit(Number(e.target.value)); setOffset(0) }}>
                  <option value={6}>6 / page</option>
                  <option value={9}>9 / page</option>
                  <option value={12}>12 / page</option>
                </select>
              </div>
            </div>
          </div>

          <div className="top__right">
            <button className="iconPill" type="button" title="Notifications">
              <Bell size={18} />
            </button>
          </div>
        </header>

        {error && (
          <div className="alert">
            <b>API error:</b> {error}
            <div className="alert__small">API base: <code>{API_BASE}</code></div>
          </div>
        )}

        <section className="gridWrap">
          <div className="gridHead">
            <div className="gridHead__left">
              <div className="gridTitle">Most popular</div>
              <div className="gridSub">{busy ? 'Loading…' : `${total} tasks • showing ${tasks.length}`}</div>
            </div>

            <div className="stats">
              <div className="stat">
                <div className="stat__num">{counts.TODO}</div>
                <div className="stat__label">To do</div>
              </div>
              <div className="stat">
                <div className="stat__num">{counts.IN_PROGRESS}</div>
                <div className="stat__label">In progress</div>
              </div>
              <div className="stat">
                <div className="stat__num">{counts.DONE}</div>
                <div className="stat__label">Done</div>
              </div>
            </div>
          </div>

          <div className="cards">
            {tasks.map(t => (
              <TaskCard
                key={t.id}
                task={t}
                onEdit={() => openEdit(t)}
                onDelete={() => onDelete(t.id)}
                onToggleStatus={() => onToggleStatus(t)}
              />
            ))}
            {!busy && tasks.length === 0 && (
              <div className="empty">
                <div className="empty__title">No tasks found</div>
                <div className="empty__sub">Try changing filters or create a new task.</div>
              </div>
            )}
          </div>

          <Pagination limit={limit} offset={offset} total={total} onChange={setOffset} />
        </section>
      </main>

      <aside className="right">
        <div className="panel">
          <div className="panel__top">
            <div className="avatarBig">A</div>
            <div>
              <div className="name">Aynaz Shateri</div>
              <div className="sub">Student • Software Engineering</div>
            </div>
          </div>

          <div className="panel__row">
            <div className="pillNum">
              <div className="pillNum__n">{total}</div>
              <div className="pillNum__t">Tasks</div>
            </div>
            <div className="pillNum">
              <div className="pillNum__n">{counts.DONE}</div>
              <div className="pillNum__t">Done</div>
            </div>
            <div className="pillNum">
              <div className="pillNum__n">{counts.IN_PROGRESS}</div>
              <div className="pillNum__t">Active</div>
            </div>
          </div>

          <div className="miniTitle">Quick actions</div>
          <div className="miniActions">
            <button className="btnSoft wide" onClick={openCreate} type="button">Create task</button>
            <button className="btnSoft wide" onClick={() => { setQ(''); setChip('all'); setOffset(0); refresh(true) }} type="button">Reset filters</button>
          </div>

          <div className="miniTitle">Tips</div>
          <div className="tip">
            <b>Status toggle:</b> use the ↔ icon on a card to cycle TODO → IN_PROGRESS → DONE.
          </div>
        </div>

        <div className="panel panel--soft">
          <div className="miniTitle">Requirements covered</div>
          <ul className="checklist">
            <li>Create / Read / Update / Delete</li>
            <li>Filter + search + pagination</li>
            <li>Status change endpoint</li>
            <li>Clean API error model</li>
          </ul>
        </div>
      </aside>

      <TaskModal
        open={modalOpen}
        mode={modalMode}
        initial={editing}
        onClose={() => setModalOpen(false)}
        onSubmit={onSubmit}
      />
    </div>
  )
}
