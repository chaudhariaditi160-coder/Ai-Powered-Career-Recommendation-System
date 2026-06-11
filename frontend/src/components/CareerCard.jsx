import React from 'react';
import { Award, ArrowRight, Bookmark, BookmarkCheck, TrendingUp, DollarSign } from 'lucide-react';

export default function CareerCard({ 
  career, 
  onSave, 
  onViewRoadmap, 
  isSaved = false 
}) {
  const formatSalary = (amt) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(amt);
  };

  return (
    <div className="glass-card rounded-2xl p-6 shadow-premium hover:shadow-premium-hover transition-all duration-300 relative overflow-hidden group">
      {/* Decorative colored glow on card hover */}
      <div className="absolute top-0 left-0 w-2 h-full bg-primary-500 group-hover:bg-accent-purple transition-colors" />
      
      <div className="flex justify-between items-start gap-4">
        <div>
          <span className="text-[10px] uppercase font-bold text-primary-500 dark:text-primary-400 tracking-widest flex items-center gap-1.5 mb-1.5">
            <Award className="w-3.5 h-3.5" /> AI Recommendation
          </span>
          <h3 className="font-bold text-lg text-slate-800 dark:text-slate-100 group-hover:text-primary-500 transition-colors">
            {career.career}
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => onSave(career.career, career.match_percentage)}
            className={`p-2 rounded-xl border transition-colors ${
              isSaved
                ? 'bg-primary-50 border-primary-200 text-primary-600 dark:bg-primary-950/40 dark:border-primary-900/50 dark:text-primary-400'
                : 'bg-white border-slate-200 text-slate-400 hover:text-slate-600 dark:bg-dark-800 dark:border-dark-700'
            }`}
            title={isSaved ? "Saved" : "Save Career"}
          >
            {isSaved ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </button>
          <div className="px-3 py-1.5 rounded-xl bg-primary-500/10 text-primary-600 dark:text-primary-400 font-bold text-sm">
            {career.match_percentage}% Match
          </div>
        </div>
      </div>

      <p className="text-xs text-slate-500 dark:text-slate-400 mt-3 line-clamp-2 leading-relaxed">
        {career.description}
      </p>

      {/* Stats list */}
      <div className="grid grid-cols-2 gap-4 mt-5 pt-4 border-t border-slate-100 dark:border-dark-800">
        <div>
          <span className="text-[10px] text-slate-400 font-medium flex items-center gap-1">
            <DollarSign className="w-3 h-3 text-slate-400" /> Avg Salary
          </span>
          <p className="text-sm font-bold text-slate-700 dark:text-slate-300 mt-0.5">
            {formatSalary(career.avg_salary)}/yr
          </p>
        </div>
        <div>
          <span className="text-[10px] text-slate-400 font-medium flex items-center gap-1">
            <TrendingUp className="w-3 h-3 text-slate-400" /> Job Growth
          </span>
          <p className="text-sm font-bold text-accent-emerald mt-0.5 flex items-center gap-1">
            +{career.growth_rate} <span className="text-[9px] px-1.5 py-0.5 rounded-md bg-accent-emerald/10 font-semibold">{career.growth_rating}</span>
          </p>
        </div>
      </div>

      {/* Skills requirements */}
      <div className="mt-4">
        <span className="text-[10px] text-slate-400 font-medium block mb-1.5">Key Core Skills:</span>
        <div className="flex flex-wrap gap-1.5">
          {career.skills_required && career.skills_required.map((skill) => (
            <span 
              key={skill}
              className="text-[9px] font-semibold px-2 py-1 rounded-lg bg-slate-100 dark:bg-dark-800 text-slate-600 dark:text-slate-300"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Action triggers */}
      <div className="mt-5 flex justify-end">
        <button
          onClick={() => onViewRoadmap(career.career)}
          className="text-xs font-semibold text-primary-500 hover:text-primary-600 flex items-center gap-1 group/btn"
        >
          View Roadmap <ArrowRight className="w-3.5 h-3.5 group-hover/btn:translate-x-0.5 transition-transform" />
        </button>
      </div>
    </div>
  );
}
