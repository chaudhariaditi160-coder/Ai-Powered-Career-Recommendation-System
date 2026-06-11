import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ClipboardList, ChevronRight, ChevronLeft, Check, BrainCircuit } from 'lucide-react';
import { assessmentAPI } from '../services/api';

export default function Assessment() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState(null);
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  // Form states
  const [careerGoal, setCareerGoal] = useState('');
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [skillRatings, setSkillRatings] = useState({
    'skl-1': 3, 'skl-2': 3, 'skl-3': 3, 'skl-4': 3, 'skl-5': 3
  });
  const [personalityRatings, setPersonalityRatings] = useState({
    'per-1': 3, 'per-2': 3, 'per-3': 3
  });
  const [techAnswers, setTechAnswers] = useState({});

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await assessmentAPI.getQuestions();
        setQuestions(res.data);
      } catch (err) {
        console.error("Failed to load questions", err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuestions();
  }, []);

  const handleInterestToggle = (interest) => {
    if (selectedInterests.includes(interest)) {
      setSelectedInterests(prev => prev.filter(i => i !== interest));
    } else {
      setSelectedInterests(prev => [...prev, interest]);
    }
  };

  const handleSkillChange = (id, val) => {
    setSkillRatings(prev => ({ ...prev, [id]: parseInt(val) }));
  };

  const handlePersonalityChange = (id, val) => {
    setPersonalityRatings(prev => ({ ...prev, [id]: parseInt(val) }));
  };

  const handleTechSelect = (qId, option) => {
    setTechAnswers(prev => ({ ...prev, [qId]: option }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const payload = {
        interests: selectedInterests,
        skills: skillRatings,
        personality: personalityRatings,
        technical: techAnswers
      };
      await assessmentAPI.submit(payload);
      
      // Navigate to results
      navigate('/results');
    } catch (err) {
      console.error("Assessment submit failed", err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="h-[70vh] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const stepsLabel = ["Goals", "Interests", "Skills", "Technical", "Personality"];

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-primary-600 flex items-center justify-center text-white">
          <ClipboardList className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-xl font-bold font-sans">Career Assessment</h2>
          <p className="text-xs text-slate-400">Answer these parameters to calculate career predictions</p>
        </div>
      </div>

      {/* Steps Progress Indicator */}
      <div className="glass-card rounded-2xl p-4 flex items-center justify-between shadow-premium border border-slate-100 dark:border-dark-800/60 overflow-x-auto whitespace-nowrap">
        {stepsLabel.map((label, idx) => (
          <div key={label} className="flex items-center gap-2">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold ${
              step > idx + 1 
                ? 'bg-accent-emerald text-white' 
                : step === idx + 1 
                  ? 'bg-primary-500 text-white' 
                  : 'bg-slate-100 dark:bg-dark-800 text-slate-400'
            }`}>
              {step > idx + 1 ? <Check className="w-3.5 h-3.5" /> : idx + 1}
            </div>
            <span className={`text-xs font-semibold ${step === idx + 1 ? 'text-slate-800 dark:text-slate-200' : 'text-slate-400'}`}>
              {label}
            </span>
            {idx < stepsLabel.length - 1 && <ChevronRight className="w-3.5 h-3.5 text-slate-300 dark:text-slate-700" />}
          </div>
        ))}
      </div>

      {/* Wizard Card Body */}
      <div className="glass-card rounded-3xl p-6 md:p-8 shadow-premium border border-slate-100 dark:border-dark-800/60 min-h-[300px] flex flex-col justify-between">
        
        {/* Step 1: Goals */}
        {step === 1 && (
          <div className="space-y-4">
            <h3 className="font-bold text-base text-slate-800 dark:text-slate-200">Step 1: Set Career Goals</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Before running predictions, do you have an initial target role in mind? You can adjust this path later.
            </p>
            <div className="space-y-1.5 pt-2">
              <label className="text-xs font-semibold text-slate-400">Target Role</label>
              <select
                value={careerGoal}
                onChange={(e) => setCareerGoal(e.target.value)}
                className="w-full bg-slate-50 dark:bg-dark-900 border border-slate-200 dark:border-dark-800 rounded-xl py-2.5 px-4 text-xs focus:outline-none focus:border-primary-500"
                id="assessment-goal-select"
              >
                <option value="">Select a general goal...</option>
                <option value="Software Engineer">Software Engineer</option>
                <option value="Data Scientist">Data Scientist</option>
                <option value="UI/UX Designer">UI/UX Designer</option>
                <option value="DevOps Engineer">DevOps Engineer</option>
                <option value="Product Manager">Product Manager</option>
                <option value="Cybersecurity Specialist">Cybersecurity Specialist</option>
                <option value="Database Administrator">Database Administrator</option>
                <option value="Digital Marketer">Digital Marketer</option>
              </select>
            </div>
          </div>
        )}

        {/* Step 2: Interests Check */}
        {step === 2 && (
          <div className="space-y-4">
            <h3 className="font-bold text-base text-slate-800 dark:text-slate-200">Step 2: Core Interests</h3>
            <p className="text-xs text-slate-400">Select elements and challenges you enjoy working on:</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {questions?.interests.map((item) => (
                <div
                  key={item.id}
                  onClick={() => handleInterestToggle(item.text)}
                  className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                    selectedInterests.includes(item.text)
                      ? 'bg-primary-500/10 border-primary-500 text-primary-600 dark:text-primary-400'
                      : 'bg-slate-50 border-slate-200 hover:bg-slate-100 dark:bg-dark-900 dark:border-dark-800 dark:hover:bg-dark-850'
                  }`}
                >
                  <p className="text-xs font-medium">{item.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Skills Ratings */}
        {step === 3 && (
          <div className="space-y-5">
            <h3 className="font-bold text-base text-slate-800 dark:text-slate-200">Step 3: Skill Self-Ratings</h3>
            <p className="text-xs text-slate-400">Rate your current self-assessment proficiency on these core topics (1 = Weak, 5 = Professional):</p>
            <div className="space-y-4 pt-2">
              {questions?.skills.map((item) => (
                <div key={item.id} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-medium text-slate-700 dark:text-slate-300">{item.text}</span>
                    <span className="font-bold text-primary-500">{skillRatings[item.id]} / 5</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={skillRatings[item.id]}
                    onChange={(e) => handleSkillChange(item.id, e.target.value)}
                    className="w-full accent-primary-500 bg-slate-200 dark:bg-dark-800 rounded-lg appearance-none h-1.5 focus:outline-none"
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Technical Questionnaire */}
        {step === 4 && (
          <div className="space-y-6">
            <h3 className="font-bold text-base text-slate-800 dark:text-slate-200">Step 4: Technical Evaluation</h3>
            <p className="text-xs text-slate-400">Solve these technical multiple choice queries:</p>
            <div className="space-y-5 pt-2">
              {questions?.technical.map((item) => (
                <div key={item.id} className="space-y-2">
                  <p className="text-xs font-semibold text-slate-700 dark:text-slate-350">{item.question}</p>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {item.options.map((opt) => (
                      <button
                        key={opt}
                        type="button"
                        onClick={() => handleTechSelect(item.id, opt)}
                        className={`p-3 text-left text-xs rounded-xl border transition-all ${
                          techAnswers[item.id] === opt
                            ? 'bg-primary-500/10 border-primary-500 text-primary-600 dark:text-primary-400 font-semibold'
                            : 'bg-slate-50 border-slate-200 hover:bg-slate-100 dark:bg-dark-900 dark:border-dark-800 dark:hover:bg-dark-850'
                        }`}
                      >
                        {opt}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 5: Personality Traits */}
        {step === 5 && (
          <div className="space-y-5">
            <h3 className="font-bold text-base text-slate-800 dark:text-slate-200">Step 5: Personality Indicators</h3>
            <p className="text-xs text-slate-400">Rate your alignment to these personal indicators (1 = Disagree, 5 = Strong Agree):</p>
            <div className="space-y-4 pt-2">
              {questions?.personality.map((item) => (
                <div key={item.id} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="font-medium text-slate-700 dark:text-slate-300">{item.text}</span>
                    <span className="font-bold text-primary-500">{personalityRatings[item.id]} / 5</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={personalityRatings[item.id]}
                    onChange={(e) => handlePersonalityChange(item.id, e.target.value)}
                    className="w-full accent-primary-500 bg-slate-200 dark:bg-dark-800 rounded-lg appearance-none h-1.5 focus:outline-none"
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action button controls */}
        <div className="flex justify-between items-center mt-10 pt-6 border-t border-slate-100 dark:border-dark-800/80">
          <button
            type="button"
            disabled={step === 1 || submitting}
            onClick={() => setStep(prev => prev - 1)}
            className="flex items-center gap-1 text-xs font-semibold text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 disabled:opacity-30 disabled:pointer-events-none"
          >
            <ChevronLeft className="w-4 h-4" /> Back
          </button>
          
          {step < 5 ? (
            <button
              type="button"
              onClick={() => setStep(prev => prev + 1)}
              className="px-5 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-xl text-xs font-semibold shadow-lg shadow-primary-500/10 flex items-center gap-1"
            >
              Next <ChevronRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              disabled={submitting}
              onClick={handleSubmit}
              className="px-6 py-2.5 bg-accent-purple hover:bg-purple-600 text-white rounded-xl text-xs font-bold shadow-lg shadow-purple-500/10 flex items-center gap-1.5"
            >
              <BrainCircuit className="w-4 h-4" /> {submitting ? 'Analyzing profile...' : 'Submit Profile'}
            </button>
          )}
        </div>

      </div>
    </div>
  );
}
