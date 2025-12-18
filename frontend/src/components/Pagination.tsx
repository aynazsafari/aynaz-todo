import React from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'

export default function Pagination(props: {
  limit: number
  offset: number
  total: number
  onChange: (offset: number) => void
}) {
  const { limit, offset, total } = props
  const page = Math.floor(offset / limit) + 1
  const pages = Math.max(1, Math.ceil(total / limit))
  const canPrev = offset > 0
  const canNext = offset + limit < total

  return (
    <div className="pager">
      <button className="pager__btn" disabled={!canPrev} onClick={() => props.onChange(Math.max(0, offset - limit))} type="button">
        <ChevronLeft size={16} /> Prev
      </button>
      <div className="pager__meta">Page <b>{page}</b> of <b>{pages}</b> • Total <b>{total}</b></div>
      <button className="pager__btn" disabled={!canNext} onClick={() => props.onChange(offset + limit)} type="button">
        Next <ChevronRight size={16} />
      </button>
    </div>
  )
}
