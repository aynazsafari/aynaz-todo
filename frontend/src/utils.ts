export function formatDateShort(iso: string | null): string {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '—'
  return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit' })
}

export function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, n))
}

export function statusLabel(status: 'TODO'|'IN_PROGRESS'|'DONE') {
  if (status === 'TODO') return 'To do'
  if (status === 'IN_PROGRESS') return 'In progress'
  return 'Done'
}
