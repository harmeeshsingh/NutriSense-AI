import { RadialBarChart, RadialBar, Legend, Tooltip, ResponsiveContainer } from 'recharts';

interface MacroChartProps {
  protein: number;
  carbs: number;
  fat: number;
  targetProtein: number;
  targetCarbs: number;
  targetFat: number;
}

export const MacroChart = ({ protein, carbs, fat, targetProtein, targetCarbs, targetFat }: MacroChartProps) => {
  const data = [
    { name: 'Protein', value: (protein / targetProtein) * 100, fill: '#ef4444' }, // Red
    { name: 'Carbs', value: (carbs / targetCarbs) * 100, fill: '#3b82f6' }, // Blue
    { name: 'Fat', value: (fat / targetFat) * 100, fill: '#eab308' }, // Yellow
  ];

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart cx="50%" cy="50%" innerRadius="30%" outerRadius="100%" barSize={15} data={data}>
          <RadialBar
            minAngle={15}
            background
            clockWise
            dataKey="value"
            cornerRadius={10}
          />
          <Tooltip />
          <Legend iconSize={10} layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0 }} />
        </RadialBarChart>
      </ResponsiveContainer>
    </div>
  );
};
