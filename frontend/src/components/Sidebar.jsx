import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  ClipboardList,
  Award,
  FileSearch,
  GitMerge,
  GitFork,
  Lock,
  LogOut
} from 'lucide-react';

export default function Sidebar({ user, onLogout }) {
  const menuItems = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: <LayoutDashboard className="w-4 h-4" />
    },
    {
      name: "Assessment",
      path: "/assessment",
      icon: <ClipboardList className="w-4 h-4" />
    },
    {
      name: "Career Results",
      path: "/results",
      icon: <Award className="w-4 h-4" />
    },
    {
      name: "Resume Analyzer",
      path: "/resume",
      icon: <FileSearch className="w-4 h-4" />
    },
    {
      name: "Skill Gap",
      path: "/skill-gap",
      icon: <GitMerge className="w-4 h-4" />
    },
    {
      name: "Roadmap",
      path: "/roadmap",
      icon: <GitFork className="w-4 h-4" />
    }
  ];

  return (
    <aside className="w-64 bg-white dark:bg-dark-900 border-r border-slate-100 dark:border-dark-800 flex flex-col h-[calc(100vh-64px)] sticky top-16 transition-colors duration-300">

      {/* Menu */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-1">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-primary-50 text-primary-600 dark:bg-primary-950/30 dark:text-primary-400'
                  : 'text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-dark-800/40 hover:text-slate-800 dark:hover:text-slate-200'
              }`
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}

        {/* Admin Section */}
        {user?.role === 'admin' && (
          <div className="pt-4 mt-4 border-t border-slate-100 dark:border-dark-800">
            <span className="px-4 text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
              Administration
            </span>

            <NavLink
              to="/admin"
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                  isActive
                    ? 'bg-purple-100 text-purple-700'
                    : 'text-slate-500 hover:bg-slate-50'
                }`
              }
            >
              <Lock className="w-4 h-4" />
              <span>Admin Dashboard</span>
            </NavLink>
          </div>
        )}
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-slate-100 dark:border-dark-800 bg-slate-50/50 dark:bg-dark-950/20">

        <div className="flex items-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
            {user?.name?.charAt(0)?.toUpperCase() || 'U'}
          </div>

          <div className="overflow-hidden">
            <p className="text-sm font-semibold truncate">
              {user?.name || 'Guest User'}
            </p>

            <p className="text-xs text-slate-400 truncate">
              {user?.email || 'guest@example.com'}
            </p>
          </div>
        </div>

        <button
          onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-red-500 text-white text-sm hover:bg-red-600 transition"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </div>
    </aside>
  );
}