import React from 'react';
import { 
  Radar, 
  RadarChart as RechartsRadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  ResponsiveContainer,
  Tooltip
} from 'recharts';

export default function RadarChart({ data, title }) {
  // Safe fallback if data is empty
  const defaultData = [
    { subject: 'Technical', A: 85, fullMark: 100 },
    { subject: 'Interests', A: 90, fullMark: 100 },
    { subject: 'Values', A: 75, fullMark: 100 },
    { subject: 'Personality', A: 80, fullMark: 100 },
    { subject: 'Growth', A: 95, fullMark: 100 },
  ];

  const chartData = data || defaultData;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-dark-800 p-3 border border-slate-100 dark:border-dark-700 rounded-xl shadow-premium text-xs">
          <p className="font-semibold text-slate-800 dark:text-slate-200">{payload[0].name}</p>
          <p className="text-primary-500 font-bold mt-1">Match: {payload[0].value}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-card rounded-2xl p-5 shadow-premium w-full h-80 flex flex-col justify-between">
      {title && (
        <h4 className="text-sm font-bold text-slate-700 dark:text-slate-300">
          {title}
        </h4>
      )}
      <div className="w-full h-64 mt-2">
        <ResponsiveContainer width="100%" height="100%">
          <RechartsRadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
            <PolarGrid stroke="#e2e8f0" strokeDasharray="3 3" className="dark:stroke-dark-700" />
            <PolarAngleAxis 
              dataKey="subject" 
              tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 500 }}
            />
            <PolarRadiusAxis 
              angle={30} 
              domain={[0, 100]} 
              tick={{ fill: '#94a3b8', fontSize: 8 }}
            />
            <Radar
              name="Skills Match"
              dataKey="A"
              stroke="#6366f1"
              fill="#6366f1"
              fillOpacity={0.25}
            />
            <Tooltip content={<CustomTooltip />} />
          </RechartsRadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
