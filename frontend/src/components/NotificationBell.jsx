import React, { useState, useEffect, useRef } from 'react';
import { Bell, Check, Award, FileText, CheckCircle, Sparkles } from 'lucide-react';
import { notificationsAPI } from '../services/api';

export default function NotificationBell() {
  const [notifications, setNotifications] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const fetchNotifications = async () => {
    try {
      const res = await notificationsAPI.getNotifications();
      setNotifications(res.data || []);
    } catch (err) {
      console.error("Failed to load notifications:", err);
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 20000); // Check every 20s
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [dropdownRef]);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const handleMarkRead = async () => {
    try {
      await notificationsAPI.markRead();
      setNotifications(prev => prev.map(n => ({ ...n, is_read: 1 })));
    } catch (err) {
      console.error(err);
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'assessment':
        return <Award className="w-4 h-4 text-primary-500" />;
      case 'learning':
        return <CheckCircle className="w-4 h-4 text-accent-emerald" />;
      case 'recommendation':
        return <Sparkles className="w-4 h-4 text-accent-purple" />;
      default:
        return <FileText className="w-4 h-4 text-slate-500" />;
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => {
          setIsOpen(!isOpen);
          if (!isOpen && unreadCount > 0) {
            handleMarkRead();
          }
        }}
        className="relative p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-dark-800 transition-all-300 focus:outline-none"
        id="notification-bell-btn"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 w-4 h-4 bg-accent-rose text-white text-[10px] font-bold rounded-full flex items-center justify-center animate-bounce">
            {unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-3 w-80 glass-card rounded-2xl shadow-xl py-2 z-50 overflow-hidden transform origin-top-right transition-all-300">
          <div className="flex items-center justify-between px-4 py-2 border-b border-slate-100 dark:border-dark-800">
            <span className="font-semibold text-sm">Notifications</span>
            {unreadCount > 0 && (
              <span className="text-xs text-primary-500 font-medium">
                {unreadCount} new
              </span>
            )}
          </div>
          <div className="max-h-64 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="px-4 py-6 text-center text-xs text-slate-400 dark:text-slate-500">
                No recent notifications
              </div>
            ) : (
              notifications.map((note) => (
                <div
                  key={note.id}
                  className={`flex gap-3 px-4 py-3 border-b border-slate-50/50 dark:border-dark-800/50 hover:bg-slate-50 dark:hover:bg-dark-800/40 transition-colors ${
                    !note.is_read ? 'bg-primary-50/20 dark:bg-primary-950/10' : ''
                  }`}
                >
                  <div className="mt-0.5 p-1.5 bg-slate-100 dark:bg-dark-800 rounded-lg h-fit">
                    {getIcon(note.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-slate-700 dark:text-slate-300 leading-snug break-words">
                      {note.message}
                    </p>
                    <span className="text-[10px] text-slate-400 dark:text-slate-500 mt-1 block">
                      {new Date(note.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
