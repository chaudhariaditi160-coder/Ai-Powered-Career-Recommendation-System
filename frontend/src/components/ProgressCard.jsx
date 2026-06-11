import React from 'react';
import { BookOpen, Award, CheckCircle, Play } from 'lucide-react';

export default function ProgressCard({ 
  course, 
  onUpdateProgress 
}) {
  const isCompleted = course.progress === 100 || course.status === 'Completed';

  return (
    <div className="glass-card rounded-2xl p-5 shadow-premium hover:shadow-premium-hover transition-all-300 flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-start gap-4 mb-2">
          <span className="text-[9px] font-bold px-2 py-1 rounded-lg bg-slate-100 dark:bg-dark-800 text-slate-500 dark:text-slate-400 uppercase tracking-wider">
            {course.level}
          </span>
          {isCompleted ? (
            <span className="flex items-center gap-1 text-[10px] font-bold text-accent-emerald bg-accent-emerald/10 px-2 py-0.5 rounded-full">
              <CheckCircle className="w-3.5 h-3.5 fill-current text-accent-emerald/10" /> Completed
            </span>
          ) : (
            <span className="text-[10px] font-bold text-primary-500 bg-primary-500/10 px-2 py-0.5 rounded-full">
              {course.progress}% Completed
            </span>
          )}
        </div>

        <h4 className="font-bold text-sm text-slate-800 dark:text-slate-100 line-clamp-2 min-h-[40px] leading-snug">
          {course.title}
        </h4>
        <p className="text-[10px] text-slate-400 mt-1 font-medium">
          Provided by {course.provider}
        </p>

        <div className="flex gap-4 text-[10px] text-slate-500 dark:text-slate-400 mt-4">
          <div>
            <span className="font-semibold block text-slate-400">Duration</span>
            <span>{course.duration}</span>
          </div>
          <div>
            <span className="font-semibold block text-slate-400">Skill target</span>
            <span className="underline decoration-primary-300 decoration-2">{course.skill}</span>
          </div>
          <div>
            <span className="font-semibold block text-slate-400">Rating</span>
            <span>⭐ {course.rating}</span>
          </div>
        </div>
      </div>

      <div className="mt-5 pt-3 border-t border-slate-100 dark:border-dark-800">
        {/* Progress Bar */}
        <div className="w-full bg-slate-100 dark:bg-dark-800 h-1.5 rounded-full overflow-hidden mb-4">
          <div 
            className="bg-primary-500 h-full rounded-full transition-all duration-500" 
            style={{ width: `${course.progress}%` }}
          />
        </div>

        <div className="flex justify-between items-center">
          {!isCompleted ? (
            <>
              <button
                onClick={() => onUpdateProgress(course.title, Math.min(course.progress + 25, 100), course.progress + 25 >= 100 ? 'Completed' : 'In Progress')}
                className="text-xs font-semibold text-primary-500 hover:text-primary-600 flex items-center gap-1"
              >
                <Play className="w-3 h-3 fill-current" /> Study Next
              </button>
              <button
                onClick={() => onUpdateProgress(course.title, 100, 'Completed')}
                className="text-[10px] font-bold text-slate-400 hover:text-accent-emerald transition-colors"
              >
                Mark Complete
              </button>
            </>
          ) : (
            <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
              <Award className="w-4 h-4 text-accent-emerald" /> Certificate earned!
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
