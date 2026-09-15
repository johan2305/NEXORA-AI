import { useEffect, useRef, useState } from 'react'
import { listNotifications, markNotificationAsRead } from '../api/notifications'

function NotificationBell() {
  const [notifications, setNotifications] = useState([])
  const [isOpen, setIsOpen] = useState(false)
  const wsRef = useRef(null)

  const unreadCount = notifications.filter((n) => !n.is_read).length

  useEffect(() => {
    async function loadInitial() {
      const data = await listNotifications()
      setNotifications(data)
    }
    loadInitial()

    const token = localStorage.getItem('nexora-access-token')
    if (!token) return

    const ws = new WebSocket(`ws://127.0.0.1:8000/notifications/ws?token=${token}`)
    wsRef.current = ws

    ws.onmessage = (event) => {
      const newNotification = JSON.parse(event.data)
      setNotifications((prev) => [
        {
          id: crypto.randomUUID(),
          is_read: false,
          created_at: new Date().toISOString(),
          ...newNotification,
        },
        ...prev,
      ])
    }

    return () => {
      ws.close()
    }
  }, [])

  async function handleOpen() {
    setIsOpen(!isOpen)
  }

  async function handleMarkAsRead(id) {
    if (!id.includes('-') || id.length < 36) return // ids temporales del WS sin persistir aún
    await markNotificationAsRead(id)
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
    )
  }

  return (
    <div className="relative">
      <button
        onClick={handleOpen}
        className="relative px-3 py-2 rounded text-sm text-text-secondary hover:text-text-primary text-left w-full flex items-center justify-between"
      >
        <span>Notificaciones</span>
        {unreadCount > 0 && (
          <span className="bg-accent text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-mono">
            {unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute left-0 bottom-full mb-2 w-72 bg-bg-surface border border-border rounded-lg shadow-lg max-h-80 overflow-y-auto z-50">
          {notifications.length === 0 ? (
            <p className="text-text-secondary text-xs p-4">Sin notificaciones todavía.</p>
          ) : (
            notifications.map((n) => (
              <button
                key={n.id}
                onClick={() => handleMarkAsRead(n.id)}
                className={`w-full text-left p-3 border-b border-border last:border-b-0 hover:bg-bg-base transition-colors ${
                  n.is_read ? 'opacity-50' : ''
                }`}
              >
                <p className="text-sm font-medium">{n.title}</p>
                <p className="text-xs text-text-secondary mt-1">{n.message}</p>
                <p className="text-xs font-mono text-text-secondary mt-1">
                  {new Date(n.created_at).toLocaleTimeString()}
                </p>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  )
}

export default NotificationBell