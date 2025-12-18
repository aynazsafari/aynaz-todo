import React from 'react'

export type Chip = { key: string; label: string }

export default function ChipBar(props: {
  chips: Chip[]
  active: string
  onChange: (key: string) => void
}) {
  return (
    <div className="chips">
      {props.chips.map(c => (
        <button
          key={c.key}
          type="button"
          className={'chip ' + (props.active === c.key ? 'is-active' : '')}
          onClick={() => props.onChange(c.key)}
        >
          {c.label}
        </button>
      ))}
    </div>
  )
}
