import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Brain, FileSearch, GitFork, ArrowRight } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-dark-950 text-slate-800 dark:text-slate-200 transition-colors duration-300">
      {/* Navbar header */}
      <nav className="h-16 px-6 max-w-7xl mx-auto flex items-center justify-between border-b border-slate-100 dark:border-dark-800/40">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => navigate('/')}>
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center text-white">
            <Sparkles className="w-4 h-4 fill-current text-white/90" />
          </div>
          <span className="font-bold text-base tracking-tight">
            Career<span className="text-primary-500">AI</span>
          </span>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/login')}
            className="text-xs font-semibold text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
          >
            Log In
          </button>
          <button 
            onClick={() => navigate('/register')}
            className="text-xs font-semibold bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-xl shadow-lg shadow-primary-500/10 hover:shadow-primary-500/25 transition-all duration-200"
          >
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero section */}
      <div className="max-w-7xl mx-auto px-6 pt-16 pb-24 md:pt-24 md:pb-32 text-center relative overflow-hidden">
        {/* Background blobs for premium depth */}
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-primary-400/10 rounded-full blur-3xl -z-10 animate-pulse" />
        <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-accent-purple/10 rounded-full blur-3xl -z-10 animate-pulse" />

        <div className="max-w-3xl mx-auto space-y-6">
          <span className="px-4 py-1.5 rounded-full bg-primary-500/10 text-primary-600 dark:text-primary-400 text-xs font-bold tracking-wide uppercase inline-flex items-center gap-1.5">
            🚀 The Future of Career Growth
          </span>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight font-sans text-slate-900 dark:text-white leading-tight">
            AI-Powered <span className="gradient-text-primary">Career Guidance</span> & Development Platform
          </h1>
          <p className="text-base md:text-lg text-slate-500 dark:text-slate-400 leading-relaxed max-w-2xl mx-auto">
            Discover your ideal professional path using advanced ML model matching based on your skills, interests, and personality. Map roadmaps, analyze resumes, and study targeted courses.
          </p>
          <div className="pt-6 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => navigate('/register')}
              className="w-full sm:w-auto px-8 py-3.5 bg-primary-600 hover:bg-primary-700 text-white font-bold rounded-2xl shadow-xl shadow-primary-500/25 hover:shadow-primary-500/40 hover:-translate-y-0.5 transition-all-300 flex items-center justify-center gap-2"
            >
              Start Free Assessment <ArrowRight className="w-5 h-5" />
            </button>
            <button
              onClick={() => navigate('/login')}
              className="w-full sm:w-auto px-8 py-3.5 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 dark:bg-dark-900 dark:border-dark-800 dark:text-slate-300 dark:hover:bg-dark-800/80 font-bold rounded-2xl transition-all duration-200 flex items-center justify-center"
            >
              Sign In to Profile
            </button>
          </div>
        </div>
      </div>

      {/* Feature section */}
      <div className="bg-slate-100/50 dark:bg-dark-900/40 py-20 border-t border-slate-100 dark:border-dark-900">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-lg mx-auto space-y-3 mb-16">
            <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white">
              Platform Features
            </h2>
            <p className="text-xs text-slate-400">
              A comprehensive system providing automated insights to jumpstart your career pivot.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Form */}
            <div className="glass-card p-6 rounded-2xl shadow-premium border border-slate-100 dark:border-dark-800/60 flex flex-col gap-4">
              <div className="w-10 h-10 rounded-xl bg-primary-500/10 text-primary-500 flex items-center justify-center">
                <Brain className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-sm text-slate-950 dark:text-white">Career Assessments</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Take personality, interest, and tech skill questionnaires to feed criteria variables into our prediction algorithms.
              </p>
            </div>
            
            {/* Prediction */}
            <div className="glass-card p-6 rounded-2xl shadow-premium border border-slate-100 dark:border-dark-800/60 flex flex-col gap-4">
              <div className="w-10 h-10 rounded-xl bg-accent-purple/10 text-accent-purple flex items-center justify-center">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-sm text-slate-950 dark:text-white">ML Recommendations</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Our Random Forest classifier model calculates match percentages to highlight your top 5 matching careers.
              </p>
            </div>

            {/* ATS Analyzer */}
            <div className="glass-card p-6 rounded-2xl shadow-premium border border-slate-100 dark:border-dark-800/60 flex flex-col gap-4">
              <div className="w-10 h-10 rounded-xl bg-accent-emerald/10 text-accent-emerald flex items-center justify-center">
                <FileSearch className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-sm text-slate-950 dark:text-white">ATS Resume Parsing</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Upload your PDF resume to check keyword compatibility, formatting ratings, and extract skills data.
              </p>
            </div>

            {/* Roadmaps */}
            <div className="glass-card p-6 rounded-2xl shadow-premium border border-slate-100 dark:border-dark-800/60 flex flex-col gap-4">
              <div className="w-10 h-10 rounded-xl bg-accent-rose/10 text-accent-rose flex items-center justify-center">
                <GitFork className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-sm text-slate-950 dark:text-white">Structured Roadmaps</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Generate beginner-to-advanced learning tracks, matching skills gaps directly to Coursera/Udemy recommendations.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-10 text-center text-xs text-slate-400 dark:text-slate-600 border-t border-slate-100 dark:border-dark-900">
        <p>© 2026 CareerAI. All rights reserved. Designed for modern professional acceleration.</p>
      </footer>
    </div>
  );
}
