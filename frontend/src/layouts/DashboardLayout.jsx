import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

export default function DashboardLayout({ user, onLogout }) {
  // Check authentication
  const token = localStorage.getItem('career_ai_token');

  // Redirect if not logged in
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-dark-950 text-slate-800 dark:text-slate-200 transition-colors duration-300">

      {/* Top Navbar */}
      <Navbar
        user={user}
        onLogout={onLogout}
      />

      <div className="flex flex-1 overflow-hidden">

        {/* Sidebar */}
        <Sidebar
          user={user}
          onLogout={onLogout}
        />

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          <Outlet />
        </main>

      </div>
    </div>
  );
}