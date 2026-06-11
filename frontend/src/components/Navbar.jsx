import React, { useState, useEffect } from 'react';
import { Sun, Moon, Sparkles, User, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import NotificationBell from './NotificationBell';

export default function Navbar({ user, onLogout }) {
  const navigate = useNavigate();
  // Persistent Theme Switch logic
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem('career_ai_theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    if (isDark) {
      document.body.classList.add('dark');
      localStorage.setItem('career_ai_theme', 'dark');
    } else {
      document.body.classList.remove('dark');
      localStorage.setItem('career_ai_theme', 'light');
    }
  }, [isDark]);

  return (
    <header className="h-16 px-6 flex items-center justify-between bg-white/70 dark:bg-dark-900/60 backdrop-blur-md border-b border-slate-100 dark:border-dark-800 sticky top-0 z-30 transition-colors duration-300">
      <div className="flex items-center gap-3">
        <div 
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 cursor-pointer group"
        >
          <div className="w-9 h-9 bg-primary-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 fill-current text-white/90" />
          </div>
          <span className="font-bold text-lg tracking-tight font-sans">
            Career<span className="text-primary-500">AI</span>
          </span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Dark Mode Switch */}
        <button
          onClick={() => setIsDark(!isDark)}
          className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-dark-800 transition-all-300 focus:outline-none"
          title={isDark ? "Light Mode" : "Dark Mode"}
          id="theme-toggle-btn"
        >
          {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>

        {/* Notifications Bell */}
        <NotificationBell />

        <div className="h-6 w-px bg-slate-200 dark:bg-dark-800" />

        {/* User profile dropdown triggers */}
        {user ? (
          <div className="flex items-center gap-3 pl-1">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-500 to-accent-purple flex items-center justify-center text-white text-xs font-semibold shadow-md">
              {user.name ? user.name[0].toUpperCase() : <User className="w-4 h-4" />}
            </div>
            <div className="hidden md:block text-left">
              <p className="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate max-w-[120px]">
                {user.name}
              </p>
              <p className="text-[10px] text-slate-400 font-medium">
                {user.role === 'admin' ? 'Administrator' : 'Premium Member'}
              </p>
            </div>
            
            <button
              onClick={onLogout}
              className="p-2 ml-1 rounded-full text-slate-400 hover:text-accent-rose hover:bg-slate-50 dark:hover:bg-dark-800/50 transition-colors"
              title="Logout"
              id="logout-btn"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <button
            onClick={() => navigate('/login')}
            className="text-xs font-semibold text-primary-500 hover:text-primary-600 transition-colors"
          >
            Sign In
          </button>
        )}
      </div>
    </header>
  );
}
