import React from 'react'
import type { Task } from '../types'
import { Calendar, Flag, Pencil, Trash2, ArrowRightLeft } from 'lucide-react'
import { formatDateShort, statusLabel } from '../utils'

export default function TaskCard(props: {
  task: Task
  onEdit: () => void
  onDelete: () => void
  onToggleStatus: () => void
}) {
  const t = props.task
  const badgeClass =
    t.status === 'DONE' ? 'badge badge--done' :
    t.status === 'IN_PROGRESS' ? 'badge badge--progress' :
    'badge badge--todo'

  return (
    <div className="card">
      <div className="card__top">
        <div className={badgeClass}>{statusLabel(t.status)}</div>
        <div className="card__actions">
          <button className="iconBtn" onClick={props.onToggleStatus} title="Change status" type="button">
            <ArrowRightLeft size={16} />
          </button>
          <button className="iconBtn" onClick={props.onEdit} title="Edit" type="button">
            <Pencil size={16} />
          </button>
          <button className="iconBtn danger" onClick={props.onDelete} title="Delete" type="button">
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      <div className="card__title">{t.title}</div>
      {t.description ? <div className="card__desc">{t.description}</div> : <div className="card__desc is-muted">No description</div>}

      <div className="card__meta">
        <span className="metaPill"><Calendar size={14} /> {formatDateShort(t.due_at)}</span>
        <span className="metaPill"><Flag size={14} /> Priority {t.priority ?? 3}</span>
      </div>
    </div>
  )
}
