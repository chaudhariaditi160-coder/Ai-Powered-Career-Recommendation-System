import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Award, 
  FileText, 
  TrendingUp, 
  BookOpen, 
  Sparkles, 
  Download, 
  Mail,
  ArrowRight,
  ShieldCheck,
  AlertCircle
} from 'lucide-react';
import { 
  authAPI, 
  predictAPI, 
  resumeAPI, 
  roadmapAPI, 
  notificationsAPI 
} from '../services/api';
import { RadarChart, BarChart } from '../components/Charts';
import CareerCard from '../components/CareerCard';

export default function Dashboard() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [resumeData, setResumeData] = useState(null);
  const [roadmapData, setRoadmapData] = useState(null);
  const [notifications, setNotifications] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [reportLoading, setReportLoading] = useState(false);
  const [emailLoading, setEmailLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load user profile details
      const profileRes = await authAPI.getProfile();
      setProfile(profileRes.data);

      // Load AI career recommendations
      const recommendRes = await predictAPI.recommend();
      setRecommendations(recommendRes.data || []);

      // Load latest resume parsed analysis
      try {
        const resumeRes = await resumeAPI.getLatest();
        setResumeData(resumeRes.data);
      } catch (e) {
        console.log("No resume uploaded yet.");
      }

      // Load learning roadmap
      try {
        const roadmapRes = await roadmapAPI.getRoadmap();
        setRoadmapData(roadmapRes.data);
      } catch (e) {
        console.log("Roadmap load skipped.");
      }

      // Load notifications
      try {
        const notesRes = await notificationsAPI.getNotifications();
        setNotifications(notesRes.data || []);
      } catch (e) {
        console.log("Notifications load skipped.");
      }

    } catch (err) {
      console.error("Failed to load dashboard data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleSaveCareer = async (careerTitle, matchPercentage) => {
    try {
      await predictAPI.saveCareer(careerTitle, matchPercentage);
      setMessage({ text: `Success! Saved path '${careerTitle}' bookmark.`, type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 4000);
    } catch (err) {
      console.error(err);
      setMessage({ text: 'Could not save career. Try again.', type: 'error' });
    }
  };

  const handleDownloadReport = async () => {
    try {
      setReportLoading(true);
      const res = await predictAPI.downloadReport();
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `career_report_${profile?.name.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("Report PDF download failed", err);
    } finally {
      setReportLoading(false);
    }
  };

  const handleEmailReport = async () => {
    try {
      setEmailLoading(true);
      await predictAPI.emailReport(profile?.email);
      setMessage({ text: `Success! Career report PDF emailed to ${profile?.email}.`, type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 4000);
    } catch (err) {
      console.error("Email report failed", err);
      setMessage({ text: 'SMTP delivery failed. Check email configurations.', type: 'error' });
    } finally {
      setEmailLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="h-[70vh] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // Pre-formatting radar data based on user assessment values
  const radarChartData = [
    { subject: 'Technical', A: profile?.assessment_score || 40, fullMark: 100 },
    { subject: 'Interests', A: profile?.career_match_percentage || 50, fullMark: 100 },
    { subject: 'Resume Fit', A: profile?.resume_score || 35, fullMark: 100 },
    { subject: 'Soft Skills', A: 75, fullMark: 100 },
    { subject: 'Growth Pot.', A: recommendations[0]?.growth_rate ? parseInt(recommendations[0]?.growth_rate) * 3 : 60, fullMark: 100 }
  ];

  // Pre-formatting salary data for top prediction
  const topCareer = recommendations[0] || { career: 'Software Engineer', entry_salary: 75000, avg_salary: 110000, senior_salary: 160000 };
  const salaryChartData = [
    { name: 'Entry-Level', salary: topCareer.entry_salary },
    { name: 'Mid-Level', salary: topCareer.avg_salary },
    { name: 'Senior-Level', salary: topCareer.senior_salary }
  ];

  const currentStep = roadmapData?.steps?.find(s => s.completion_percentage < 100) || roadmapData?.steps?.[0];
  const nextRecommendedStep = currentStep?.recommended_courses?.[0];

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-primary-600 to-indigo-800 text-white shadow-xl shadow-primary-500/10">
        <div className="space-y-1">
          <h2 className="text-xl font-bold flex items-center gap-2">
            Welcome back, {profile?.name}! 👋
          </h2>
          <p className="text-xs text-primary-100">
            Current Target Goal: <span className="font-semibold underline decoration-accent-purple decoration-2">{profile?.career_goal || 'Not specified. Run the Assessment to set.'}</span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleDownloadReport}
            disabled={reportLoading}
            className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 backdrop-blur-md transition-all"
          >
            <Download className="w-4 h-4" /> {reportLoading ? 'Compiling PDF...' : 'Download Report'}
          </button>
          <button
            onClick={handleEmailReport}
            disabled={emailLoading}
            className="px-4 py-2 bg-primary-500 hover:bg-primary-400 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 shadow-lg shadow-primary-500/10 transition-all"
          >
            <Mail className="w-4 h-4" /> {emailLoading ? 'Emailing...' : 'Email Report'}
          </button>
        </div>
      </div>

      {message.text && (
        <div className={`p-4 rounded-xl text-xs flex items-center gap-2.5 ${
          message.type === 'success' 
            ? 'bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald' 
            : 'bg-accent-rose/10 border border-accent-rose/20 text-accent-rose'
        }`}>
          <ShieldCheck className="w-4 h-4" />
          <span>{message.text}</span>
        </div>
      )}

      {/* Top Statistics Indicators Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        <div className="glass-card rounded-2xl p-5 shadow-premium border border-slate-100 dark:border-dark-800/60 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-primary-500/10 text-primary-500 flex items-center justify-center">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider block">Career Match</span>
            <span className="text-xl font-bold text-slate-800 dark:text-white">{profile?.career_match_percentage}%</span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-5 shadow-premium border border-slate-100 dark:border-dark-800/60 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-accent-emerald/10 text-accent-emerald flex items-center justify-center">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider block">Resume ATS</span>
            <span className="text-xl font-bold text-slate-800 dark:text-white">{profile?.resume_score}/100</span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-5 shadow-premium border border-slate-100 dark:border-dark-800/60 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-accent-purple/10 text-accent-purple flex items-center justify-center">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider block">Learning Progress</span>
            <span className="text-xl font-bold text-slate-800 dark:text-white">{roadmapData?.overall_progress || 0}%</span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-5 shadow-premium border border-slate-100 dark:border-dark-800/60 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-accent-amber/10 text-accent-amber flex items-center justify-center">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider block">Assessment Score</span>
            <span className="text-xl font-bold text-slate-800 dark:text-white">{profile?.assessment_score}/100</span>
          </div>
        </div>
      </div>

      {/* Middle Visual Section: Charts comparisons */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RadarChart data={radarChartData} title="Comprehensive Competency mapping" />
        <BarChart data={salaryChartData} title={`Salary Benchmarks for ${topCareer.career}`} />
      </div>

      {/* Main Career recommendations lists */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold">Top AI Career Match Recommendations</h3>
          <button 
            onClick={() => navigate('/results')}
            className="text-xs text-primary-500 hover:text-primary-600 font-semibold flex items-center gap-0.5"
          >
            Analyze All <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {recommendations.length === 0 ? (
          <div className="glass-card p-10 text-center rounded-2xl border border-dashed border-slate-200 dark:border-dark-800">
            <p className="text-sm text-slate-500">Run the technical assessment questionnaire to populate model matches.</p>
            <button 
              onClick={() => navigate('/assessment')}
              className="mt-4 px-4 py-2 bg-primary-600 text-white rounded-xl text-xs font-semibold shadow-lg hover:bg-primary-700 transition"
            >
              Start Assessment
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {recommendations.slice(0, 2).map((item) => (
              <CareerCard 
                key={item.career} 
                career={item} 
                onSave={handleSaveCareer}
                onViewRoadmap={(path) => navigate('/roadmap')}
              />
            ))}
          </div>
        )}
      </div>

      {/* Resume Analyzer details + roadmap tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Resume status widget */}
        <div className="glass-card rounded-2xl p-6 shadow-premium border border-slate-100 dark:border-dark-800/60 space-y-4">
          <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200">Resume & ATS Analysis</h4>
          {resumeData?.has_resume ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3.5 bg-slate-50 dark:bg-dark-950/40 rounded-xl">
                <div>
                  <p className="text-xs font-bold text-slate-800 dark:text-slate-200 truncate max-w-[200px]">
                    📂 {resumeData.filename}
                  </p>
                  <p className="text-[10px] text-slate-400">Strength: <span className={`font-semibold ${resumeData.resume_strength === 'Strong' ? 'text-accent-emerald' : 'text-accent-rose'}`}>{resumeData.resume_strength}</span></p>
                </div>
                <div className="text-right">
                  <span className="text-lg font-bold text-primary-500">{resumeData.ats_score}%</span>
                  <p className="text-[9px] text-slate-400">Compatibility</p>
                </div>
              </div>
              <div className="space-y-1.5">
                <span className="text-[10px] text-slate-400 block font-medium">Missing Skills Identified:</span>
                <div className="flex flex-wrap gap-1">
                  {resumeData.missing_skills?.slice(0, 5).map(skill => (
                    <span key={skill} className="text-[9px] font-semibold px-2 py-0.5 rounded-lg bg-accent-rose/10 text-accent-rose">
                      {skill}
                    </span>
                  ))}
                  {(!resumeData.missing_skills || resumeData.missing_skills.length === 0) && (
                    <span className="text-xs text-accent-emerald font-medium">Perfect! No skill gaps found.</span>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-6 text-center border border-dashed border-slate-200 dark:border-dark-800 rounded-xl space-y-3">
              <AlertCircle className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-xs text-slate-500">Scan your resume PDF to calculate formatting score and skill gaps.</p>
              <button
                onClick={() => navigate('/resume')}
                className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-dark-800 dark:hover:bg-dark-750 rounded-xl text-[11px] font-bold transition"
              >
                Upload Resume
              </button>
            </div>
          )}
        </div>

        {/* Learning roadmap step tracker */}
        <div className="glass-card rounded-2xl p-6 shadow-premium border border-slate-100 dark:border-dark-800/60 space-y-4">
          <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200 font-sans">Next Recommended Step</h4>
          {nextRecommendedStep ? (
            <div className="space-y-4">
              <div className="p-4 bg-primary-500/5 border border-primary-500/10 rounded-xl">
                <span className="text-[9px] uppercase font-extrabold text-primary-500 tracking-widest block mb-1">
                  Target Course
                </span>
                <h5 className="font-bold text-xs text-slate-800 dark:text-slate-100">
                  {nextRecommendedStep.title}
                </h5>
                <p className="text-[10px] text-slate-400 mt-1">
                  Offered by {nextRecommendedStep.provider} | Duration: {nextRecommendedStep.duration}
                </p>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-[10px] text-slate-400 block">Stage level:</span>
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300">{currentStep?.stage}</span>
                </div>
                <button
                  onClick={() => navigate('/roadmap')}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-xs font-bold shadow-lg shadow-primary-500/10 transition"
                >
                  Go to Roadmap
                </button>
              </div>
            </div>
          ) : (
            <div className="p-6 text-center border border-dashed border-slate-200 dark:border-dark-800 rounded-xl space-y-3">
              <BookOpen className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-xs text-slate-500">Configure your target career goal and scan your skills to unlock custom roadmaps.</p>
              <button
                onClick={() => navigate('/assessment')}
                className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 dark:bg-dark-800 dark:hover:bg-dark-750 rounded-xl text-[11px] font-bold transition"
              >
                Configure Goal
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Notifications log widget */}
      <div className="glass-card rounded-2xl p-6 shadow-premium border border-slate-100 dark:border-dark-800/60 space-y-4">
        <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200">Latest Alerts & Activity</h4>
        <div className="space-y-3">
          {notifications.slice(0, 3).map((note) => (
            <div key={note.id} className="flex gap-3 text-xs leading-relaxed py-1">
              <span className="text-[10px] font-semibold text-slate-400 dark:text-slate-500 shrink-0 w-12">
                {new Date(note.created_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}
              </span>
              <p className="text-slate-600 dark:text-slate-350">{note.message}</p>
            </div>
          ))}
          {notifications.length === 0 && (
            <p className="text-xs text-slate-400 text-center py-4">No recent activity logged.</p>
          )}
        </div>
      </div>
    </div>
  );
}
