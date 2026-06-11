import React from 'react';
import { 
  PieChart as RechartsPieChart, 
  Pie, 
  Cell, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';

export default function PieChart({ data, title }) {
  const defaultData = [
    { name: 'Completed', value: 3 },
    { name: 'In Progress', value: 4 },
    { name: 'Not Started', value: 5 },
  ];

  const COLORS = ['#10b981', '#6366f1', '#cbd5e1']; // Emerald, Indigo, Slate
  const chartData = data || defaultData;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-dark-800 p-2.5 border border-slate-100 dark:border-dark-700 rounded-xl shadow-premium text-xs">
          <p className="font-semibold text-slate-800 dark:text-slate-200">{payload[0].name}</p>
          <p className="text-primary-500 font-bold mt-0.5">Count: {payload[0].value}</p>
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
          <RechartsPieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="48%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend 
              verticalAlign="bottom" 
              height={36} 
              iconType="circle"
              iconSize={8}
              tick={{ fill: '#94a3b8', fontSize: 10 }}
            />
          </RechartsPieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
