import React from 'react';
import { 
  BarChart as RechartsBarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';

export default function BarChart({ data, title }) {
  const defaultData = [
    { name: 'Entry-Level', salary: 65000 },
    { name: 'Mid-Level', salary: 95000 },
    { name: 'Senior-Level', salary: 145000 },
  ];

  const chartData = data || defaultData;

  const formatYAxis = (value) => {
    return `$${value / 1000}k`;
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-dark-800 p-3 border border-slate-100 dark:border-dark-700 rounded-xl shadow-premium text-xs">
          <p className="font-semibold text-slate-800 dark:text-slate-200">{payload[0].name}</p>
          <p className="text-primary-500 font-bold mt-1">
            Salary: {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(payload[0].value)}
          </p>
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
          <RechartsBarChart
            data={chartData}
            margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" className="dark:stroke-dark-800" vertical={false} />
            <XAxis 
              dataKey="name" 
              tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 500 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis 
              tickFormatter={formatYAxis}
              tick={{ fill: '#94a3b8', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="salary" 
              fill="#6366f1" 
              radius={[8, 8, 0, 0]}
              maxBarSize={45}
            />
          </RechartsBarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
