import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { GitMerge, CheckCircle, AlertCircle, BookOpen, Sparkles, ArrowRight } from 'lucide-react';
import { resumeAPI, authAPI, roadmapAPI } from '../services/api';
import ProgressCard from '../components/ProgressCard';

export default function SkillGap() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [roadmapData, setRoadmapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [successMsg, setSuccessMsg] = useState('');

  const loadGapData = async () => {
    try {
      setLoading(true);
      
      const profileRes = await authAPI.getProfile();
      setProfile(profileRes.data);

      const resumeRes = await resumeAPI.getLatest();
      setResumeData(resumeRes.data);

      // Load matching roadmap course recommendations
      const roadmapRes = await roadmapAPI.getRoadmap();
      setRoadmapData(roadmapRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGapData();
  }, []);

  const handleUpdateProgress = async (courseName, progress, status) => {
    try {
      await roadmapAPI.updateProgress(courseName, progress, status);
      setSuccessMsg(`Progress updated for course: ${courseName}`);
      
      // Reload states
      const roadmapRes = await roadmapAPI.getRoadmap();
      setRoadmapData(roadmapRes.data);
      
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

  const missingSkills = resumeData?.missing_skills || [];
  const possessedSkills = resumeData?.extracted_skills || [];

  return (
    <div className="space-y-8 max-w-7xl mx-auto font-sans">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary-600 flex items-center justify-center text-white">
          <GitMerge className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-xl font-bold">Skill Gap Analysis</h2>
          <p className="text-xs text-slate-400">Evaluate alignment against requirements for: <span className="font-semibold">{profile?.career_goal || 'General Development'}</span></p>
        </div>
      </div>

      {successMsg && (
        <div className="p-4 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald text-xs font-medium rounded-xl">
          {successMsg}
        </div>
      )}

      {!resumeData?.has_resume ? (
        <div className="glass-card rounded-3xl p-10 text-center border border-slate-100 dark:border-dark-800 space-y-4">
          <AlertCircle className="w-12 h-12 text-slate-350 dark:text-slate-700 mx-auto" />
          <h3 className="font-bold text-sm">Resume Data Missing</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            We require an uploaded resume PDF to parse your current skill metrics. Upload a resume file to generate comparison lists.
          </p>
          <button
            onClick={() => navigate('/resume')}
            className="px-5 py-2.5 bg-primary-600 text-white rounded-xl text-xs font-semibold shadow-lg hover:bg-primary-700 transition"
          >
            Go to Resume Analyzer
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
          
          {/* Possembled & Missing Lists */}
          <div className="lg:col-span-1 space-y-6">
            <div className="glass-card rounded-3xl p-6 border border-slate-100 dark:border-dark-800 shadow-premium space-y-6">
              
              {/* Possessed Skills */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wide flex items-center gap-1.5">
                  <CheckCircle className="w-4 h-4 text-accent-emerald" /> Possessed Skills ({possessedSkills.length})
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {possessedSkills.map(skill => (
                    <span key={skill} className="text-xs font-medium px-2.5 py-1 rounded-xl bg-slate-100 dark:bg-dark-800 text-slate-700 dark:text-slate-300">
                      {skill}
                    </span>
                  ))}
                  {possessedSkills.length === 0 && <span className="text-xs text-slate-400">None detected</span>}
                </div>
              </div>

              {/* Missing Skills Gaps */}
              <div className="space-y-3 pt-4 border-t border-slate-100 dark:border-dark-800/85">
                <h4 className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wide flex items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 text-accent-rose" /> Missing Skill Gaps ({missingSkills.length})
                </h4>
                <div className="flex flex-wrap gap-1.5">
                  {missingSkills.map(skill => (
                    <span key={skill} className="text-xs font-bold px-2.5 py-1 rounded-xl bg-accent-rose/10 text-accent-rose">
                      {skill}
                    </span>
                  ))}
                  {missingSkills.length === 0 && <span className="text-xs text-accent-emerald font-semibold">Perfect alignment! No gaps.</span>}
                </div>
              </div>

            </div>
          </div>

          {/* Recommended Course recommendations */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-700 dark:text-slate-350 uppercase tracking-wide flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-primary-500" /> Target Courses for Missing Skills
              </h3>
              <button
                onClick={() => navigate('/roadmap')}
                className="text-xs font-semibold text-primary-500 hover:text-primary-600 flex items-center gap-0.5"
              >
                View Roadmap <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {missingSkills.length === 0 ? (
              <div className="glass-card rounded-3xl p-10 text-center border border-slate-100 dark:border-dark-800">
                <Sparkles className="w-10 h-10 text-primary-500 mx-auto mb-2" />
                <h4 className="font-bold text-sm">Perfect Skill Match Alignment!</h4>
                <p className="text-xs text-slate-400 mt-1">
                  You possess all core competencies mapped by our models for this target role. Check your mock interview page to practice!
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {/* Aggregate all step recommended courses in a flat map */}
                {roadmapData?.steps?.flatMap(step => step.recommended_courses).filter(c => missingSkills.includes(c.skill)).slice(0, 4).map((course, idx) => (
                  <ProgressCard 
                    key={course.id || idx}
                    course={course}
                    onUpdateProgress={handleUpdateProgress}
                  />
                ))}
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
}
