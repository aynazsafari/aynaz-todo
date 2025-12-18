import React, { useEffect, useMemo, useState } from 'react'
import type { Task } from '../types'
import { X } from 'lucide-react'

export default function TaskModal(props: {
  open: boolean
  mode: 'create' | 'edit'
  initial?: Task | null
  onClose: () => void
  onSubmit: (payload: { title: string; description: string | null; priority: number | null; due_at: string | null }) => Promise<void>
}) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState<string | null>(null)
  const [priority, setPriority] = useState<number>(3)
  const [due, setDue] = useState<string>('')

  useEffect(() => {
    if (!props.open) return
    if (props.mode === 'edit' && props.initial) {
      setTitle(props.initial.title)
      setDescription(props.initial.description ?? null)
      setPriority(props.initial.priority ?? 3)
      setDue(props.initial.due_at ? props.initial.due_at.slice(0, 10) : '')
    } else {
      setTitle('')
      setDescription(null)
      setPriority(3)
      setDue('')
    }
  }, [props.open, props.mode, props.initial])

  const canSubmit = useMemo(() => title.trim().length > 0, [title])

  if (!props.open) return null

  return (
    <div className="modalOverlay" role="dialog" aria-modal="true">
      <div className="modal">
        <div className="modal__head">
          <div>
            <div className="modal__title">{props.mode === 'create' ? 'Create a task' : 'Edit task'}</div>
            <div className="modal__sub">Connected to your backend (CRUD).</div>
          </div>
          <button className="iconBtn" onClick={props.onClose} title="Close" type="button"><X size={18} /></button>
        </div>

        <div className="modal__grid">
          <label className="field">
            <span className="field__label">Title *</span>
            <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g., Final report for Software Engineering" />
          </label>

          <label className="field">
            <span className="field__label">Priority (1–5)</span>
            <input className="input" type="number" min={1} max={5} value={priority} onChange={(e) => setPriority(Number(e.target.value))} />
          </label>

          <label className="field field--wide">
            <span className="field__label">Description</span>
            <textarea className="input textarea" value={description ?? ''} onChange={(e) => setDescription(e.target.value || null)} placeholder="Optional notes..." />
          </label>

          <label className="field">
            <span className="field__label">Due date</span>
            <input className="input" type="date" value={due} onChange={(e) => setDue(e.target.value)} />
          </label>
        </div>

        <div className="modal__foot">
          <button className="btnGhost" onClick={props.onClose} type="button">Cancel</button>
          <button
            className="btnPrimary"
            disabled={!canSubmit}
            onClick={() => props.onSubmit({
              title: title.trim(),
              description,
              priority: Number.isFinite(priority) ? priority : 3,
              due_at: due ? new Date(due + 'T00:00:00.000Z').toISOString() : null,
            })}
            type="button"
          >
            {props.mode === 'create' ? 'Create' : 'Save changes'}
          </button>
        </div>
      </div>
    </div>
  )
}
