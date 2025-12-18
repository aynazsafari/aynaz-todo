import React from 'react'
import { Home, LayoutGrid, ListChecks, Settings, User2, Search, Sparkles } from 'lucide-react'

export default function Sidebar(props: { active: string; onActive: (k: string) => void }) {
  const items = [
    { key: 'home', icon: Home, label: 'Home' },
    { key: 'discover', icon: LayoutGrid, label: 'Explore' },
    { key: 'tasks', icon: ListChecks, label: 'Tasks' },
    { key: 'search', icon: Search, label: 'Search' },
    { key: 'profile', icon: User2, label: 'Profile' },
    { key: 'settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <aside className="sb">
      <div className="sb__logo" title="Aynaz To-Do">
        <div className="sb__logoIcon"><Sparkles size={18} /></div>
      </div>

      <nav className="sb__nav">
        {items.map(it => {
          const Icon = it.icon
          const active = props.active === it.key
          return (
            <button
              key={it.key}
              className={'sb__btn ' + (active ? 'is-active' : '')}
              onClick={() => props.onActive(it.key)}
              aria-label={it.label}
              title={it.label}
              type="button"
            >
              <Icon size={18} />
            </button>
          )
        })}
      </nav>

      <div className="sb__avatar" title="Aynaz">
        <span>A</span>
      </div>
    </aside>
  )
}
