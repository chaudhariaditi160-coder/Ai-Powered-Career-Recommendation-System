import React, { useState, useEffect } from 'react';
import { GitFork, Check, Award, BookOpen, AlertCircle, HelpCircle } from 'lucide-react';
import { roadmapAPI } from '../services/api';
import ProgressCard from '../components/ProgressCard';

export default function Roadmap() {
const [roadmap, setRoadmap] = useState(null);
const [loading, setLoading] = useState(false);
const [successMsg, setSuccessMsg] = useState('');

const [selectedCareer, setSelectedCareer] = useState('');
const [showRoadmap, setShowRoadmap] = useState(false);

const loadRoadmap = async (selectedCareer) => {
  try {
    setLoading(true);

    const res = await roadmapAPI.getRoadmap(selectedCareer);
setRoadmap(res.data);

    setRoadmap(res.data);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};

  const handleUpdateProgress = async (courseName, progress, status) => {
    try {
      await roadmapAPI.updateProgress(courseName, progress, status);
      setSuccessMsg(`Status updated: ${courseName} is now ${progress}% completed.`);
      
      // Reload details
      const res = await roadmapAPI.getRoadmap();
      setRoadmap(res.data);
      
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="h-[70vh] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto font-sans">
      {!showRoadmap && (
  <div className="bg-white rounded-3xl p-8 shadow-lg border">
    <h2 className="text-3xl font-bold mb-4">
      Choose Your Career Path
    </h2>

    <p className="text-slate-500 mb-6">
      Select a career and generate a personalized roadmap.
    </p>

    <select
  value={selectedCareer}
  onChange={(e) => setSelectedCareer(e.target.value)}
  className="w-full p-3 border rounded-xl"
>
  <option value="">Select Career</option>

  <option value="Software Engineer">
    Software Engineer
  </option>

  <option value="Data Scientist">
    Data Scientist
  </option>

  <option value="UI/UX Designer">
    UI/UX Designer
  </option>

  <option value="DevOps Engineer">
    DevOps Engineer
  </option>

  <option value="Product Manager">
    Product Manager
  </option>

  <option value="Cybersecurity Specialist">
    Cybersecurity Specialist
  </option>

  <option value="Database Administrator">
    Database Administrator
  </option>

  <option value="Digital Marketer">
    Digital Marketer
  </option>
</select>

    <button
      className="mt-6 bg-primary-600 text-white px-6 py-3 rounded-xl"
      disabled={!selectedCareer}
      onClick={() => {
  loadRoadmap(selectedCareer);
  setShowRoadmap(true);
}}
    >
      Generate Roadmap
    </button>
  </div>
)}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary-600 flex items-center justify-center text-white">
            <GitFork className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Learning Roadmap</h2>
            <p className="text-xs text-slate-400">Personalized timeline for target role: <span className="font-semibold">{roadmap?.career_path}</span></p>
          </div>
        </div>

        {/* Global tracker metric */}
        <div className="flex items-center gap-4 bg-white dark:bg-dark-900 border border-slate-100 dark:border-dark-800 rounded-2xl p-4 shadow-premium shrink-0">
          <div className="text-right">
            <span className="text-sm font-bold text-slate-800 dark:text-slate-200">Overall Progress</span>
            <p className="text-[10px] text-slate-400">Total skills completed</p>
          </div>
          <div className="w-12 h-12 rounded-full border-4 border-primary-500 border-t-slate-200 dark:border-t-dark-800 flex items-center justify-center text-xs font-bold shadow-md">
            {roadmap?.overall_progress}%
          </div>
        </div>
      </div>

      {successMsg && (
        <div className="p-4 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald text-xs font-medium rounded-xl">
          {successMsg}
        </div>
      )}

      {/* Main Roadmap Steps timeline */}
      <div className="space-y-12 relative before:absolute before:top-2 before:left-[19px] before:bottom-0 before:w-0.5 before:bg-slate-200 before:dark:bg-dark-800">
        {roadmap?.steps?.map((step, idx) => (
          <div key={step.stage} className="relative pl-12 space-y-6">
            
            {/* Timeline node */}
            <div className={`absolute top-0.5 left-0 w-10 h-10 rounded-full border-4 border-slate-50 dark:border-dark-950 flex items-center justify-center text-white shadow-md z-10 transition-colors ${
              step.completion_percentage === 100 
                ? 'bg-accent-emerald' 
                : step.completion_percentage > 0 
                  ? 'bg-primary-500 animate-pulse' 
                  : 'bg-slate-300 dark:bg-dark-800 text-slate-500'
            }`}>
              {step.completion_percentage === 100 ? <Check className="w-5 h-5 stroke-[3]" /> : idx + 1}
            </div>

            {/* Step summary card */}
            <div className="glass-card rounded-3xl p-6 border border-slate-100 dark:border-dark-800/80 shadow-premium space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <span className="text-[9px] uppercase font-extrabold text-primary-500 tracking-wider block">
                    Stage {idx + 1} - {step.stage} Level
                  </span>
                  <h3 className="font-bold text-base text-slate-800 dark:text-slate-100">
                    {step.title}
                  </h3>
                </div>
                <div className="text-right">
                  <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                    {step.completion_percentage}% completed
                  </span>
                  <div className="w-32 bg-slate-100 dark:bg-dark-800 h-1 rounded-full overflow-hidden mt-1.5">
                    <div className="bg-primary-500 h-full rounded-full" style={{ width: `${step.completion_percentage}%` }} />
                  </div>
                </div>
              </div>

              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-2xl">
                {step.description}
              </p>

              {/* Skill mapping inside this stage */}
              <div className="pt-2">
                <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider block mb-2">Stage Skills check</span>
                <div className="flex flex-wrap gap-1.5">
                  {step.skills.map(skill => {
                    const hasSkill = step.completed_skills.includes(skill);
                    return (
                      <span 
                        key={skill}
                        className={`text-[10px] font-semibold px-2.5 py-1 rounded-xl flex items-center gap-1 ${
                          hasSkill
                            ? 'bg-accent-emerald/10 text-accent-emerald'
                            : 'bg-accent-rose/5 text-slate-400 dark:text-slate-500 border border-slate-200/40 dark:border-dark-800/40'
                        }`}
                      >
                        {hasSkill && <Check className="w-3 h-3 stroke-[3]" />}
                        {skill}
                      </span>
                    );
                  })}
                </div>
              </div>

              {/* Course recommendations list */}
              {step.recommended_courses?.length > 0 && (
                <div className="pt-4 border-t border-slate-100 dark:border-dark-800/60">
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider flex items-center gap-1.5 mb-4">
                    <BookOpen className="w-3.5 h-3.5 text-primary-500" /> Recommended Study modules
                  </span>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {step.recommended_courses.map((course) => (
                      <ProgressCard 
                        key={course.title}
                        course={course}
                        onUpdateProgress={handleUpdateProgress}
                      />
                    ))}
                  </div>
                </div>
              )}

            </div>

          </div>
        ))}
      </div>
    </div>
  );
}
