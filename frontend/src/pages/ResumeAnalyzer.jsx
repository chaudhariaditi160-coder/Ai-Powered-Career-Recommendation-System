import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileSearch, Upload, CheckCircle2, AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react';
import { resumeAPI } from '../services/api';

export default function ResumeAnalyzer() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');

  const loadLatestAnalysis = async () => {
    try {
      const res = await resumeAPI.getLatest();
      if (res.data && res.data.has_resume) {
        setAnalysis(res.data);
      }
    } catch (err) {
      console.log("No resume analyzed yet.");
    }
  };

  useEffect(() => {
    loadLatestAnalysis();
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF file first.');
      return;
    }
    
    setError('');
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await resumeAPI.upload(formData);
      setAnalysis(res.data.analysis);
      loadLatestAnalysis();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to analyze resume. Verify it is a valid PDF/TXT file.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto font-sans">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary-600 flex items-center justify-center text-white">
          <FileSearch className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-xl font-bold">Resume & ATS Analyzer</h2>
          <p className="text-xs text-slate-400">Evaluate formatting layout, scan skills, and calculate ATS compatibility ratings</p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-accent-rose/10 border border-accent-rose/20 text-accent-rose text-xs font-semibold rounded-xl">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
        {/* Upload form container */}
        <div className="glass-card p-6 rounded-3xl border border-slate-100 dark:border-dark-800 shadow-premium flex flex-col justify-between min-h-[320px]">
          <div>
            <h3 className="font-bold text-sm text-slate-800 dark:text-slate-200 mb-3">Upload PDF Resume</h3>
            <form onSubmit={handleUpload} className="space-y-4">
              <div className="border border-dashed border-slate-200 dark:border-dark-800 hover:border-primary-500 rounded-2xl p-6 text-center cursor-pointer transition-colors relative">
                <input
                  type="file"
                  accept=".pdf,.txt"
                  onChange={handleFileChange}
                  className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
                  id="resume-file-input"
                />
                <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                <p className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  {file ? file.name : 'Choose file or drag here'}
                </p>
                <p className="text-[9px] text-slate-400 mt-1">Supported files: PDF, TXT (Max 5MB)</p>
              </div>

              <button
                type="submit"
                disabled={uploading || !file}
                className="w-full bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 rounded-xl text-xs shadow-lg shadow-primary-500/10 hover:shadow-primary-500/20 transition-all duration-200 disabled:opacity-40"
                id="resume-upload-btn"
              >
                {uploading ? 'Parsing Resume...' : 'Start Scan'}
              </button>
            </form>
          </div>

          <div className="text-[10px] text-slate-400 mt-6 leading-relaxed border-t border-slate-100 dark:border-dark-800/80 pt-4">
            🔒 Files are processed securely. Your data stays confidential and is used solely for skill matching evaluations.
          </div>
        </div>

        {/* Scan reports container */}
        <div className="md:col-span-2 space-y-6">
          {!analysis ? (
            <div className="glass-card rounded-3xl p-10 text-center border border-slate-100 dark:border-dark-800 h-80 flex flex-col items-center justify-center space-y-4">
              <FileSearch className="w-12 h-12 text-slate-300 dark:text-slate-700" />
              <div>
                <h4 className="font-bold text-sm">No analysis reports found</h4>
                <p className="text-xs text-slate-400 mt-1 max-w-sm">
                  Upload your CV in PDF format. We will compile score metrics and flag missing skills compared to target paths.
                </p>
              </div>
            </div>
          ) : (
            <div className="glass-card rounded-3xl p-6 md:p-8 border border-slate-100 dark:border-dark-800 shadow-premium space-y-6">
              
              {/* ATS score meters */}
              <div className="flex items-center justify-between gap-6 pb-6 border-b border-slate-100 dark:border-dark-800/80">
                <div className="space-y-1">
                  <h3 className="font-bold text-base">ATS Compatibility Report</h3>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full inline-block ${
                    analysis.resume_strength === 'Strong'
                      ? 'bg-accent-emerald/10 text-accent-emerald'
                      : analysis.resume_strength === 'Medium'
                        ? 'bg-primary-500/10 text-primary-500'
                        : 'bg-accent-rose/10 text-accent-rose'
                  }`}>
                    {analysis.resume_strength} Profile Strength
                  </span>
                </div>
                <div className="text-center">
                  <div className="w-20 h-20 rounded-full border-4 border-primary-500 border-t-primary-200 flex items-center justify-center text-xl font-bold text-slate-800 dark:text-white shadow-lg shadow-primary-500/15">
                    {analysis.ats_score}%
                  </div>
                  <p className="text-[9px] text-slate-400 mt-1.5 font-medium">ATS Match Score</p>
                </div>
              </div>

              {/* Identified Skills list */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wide">Identified Competencies</h4>
                <div className="flex flex-wrap gap-1.5">
                  {analysis.extracted_skills?.map(skill => (
                    <span key={skill} className="text-xs font-medium px-2.5 py-1 rounded-xl bg-slate-100 dark:bg-dark-800 text-slate-700 dark:text-slate-350">
                      {skill}
                    </span>
                  ))}
                  {(!analysis.extracted_skills || analysis.extracted_skills.length === 0) && (
                    <p className="text-xs text-slate-400">No matching skills detected in CV text.</p>
                  )}
                </div>
              </div>

              {/* Formatting checks list */}
              <div className="space-y-3 pt-2">
                <h4 className="text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wide">Structure & Layout Integrity</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="flex items-center gap-2 p-3 bg-slate-50 dark:bg-dark-900/60 rounded-xl">
                    <CheckCircle2 className="w-4 h-4 text-accent-emerald shrink-0" />
                    <span>Standard section labels matched</span>
                  </div>
                  <div className="flex items-center gap-2 p-3 bg-slate-50 dark:bg-dark-900/60 rounded-xl">
                    <CheckCircle2 className="w-4 h-4 text-accent-emerald shrink-0" />
                    <span>Appropriate word count length</span>
                  </div>
                  <div className="flex items-center gap-2 p-3 bg-slate-50 dark:bg-dark-900/60 rounded-xl">
                    <CheckCircle2 className="w-4 h-4 text-accent-emerald shrink-0" />
                    <span>Machine-readable formatting</span>
                  </div>
                  <div className="flex items-center gap-2 p-3 bg-slate-50 dark:bg-dark-900/60 rounded-xl">
                    <CheckCircle2 className="w-4 h-4 text-accent-emerald shrink-0" />
                    <span>No layout columns warnings</span>
                  </div>
                </div>
              </div>

              {/* Action routes */}
              <div className="flex justify-end pt-4 border-t border-slate-100 dark:border-dark-800/80">
                <button
                  onClick={() => navigate('/skill-gap')}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-xs font-semibold shadow-lg shadow-primary-500/10 flex items-center gap-1.5 transition"
                >
                  Analyze Skill Gap <ShieldCheck className="w-4 h-4" />
                </button>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
}
