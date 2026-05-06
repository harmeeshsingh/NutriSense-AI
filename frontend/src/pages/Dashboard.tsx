import { MacroChart } from '../components/MacroChart';

export const Dashboard = () => {
  // Mock data for initial render
  const macroData = {
    protein: 65, targetProtein: 150,
    carbs: 120, targetCarbs: 200,
    fat: 45, targetFat: 70,
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Today's Overview</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-semibold mb-4">Macro Progress</h2>
          <MacroChart {...macroData} />
        </div>
        
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
          <div className="text-center">
            <p className="text-gray-500 mb-1">Calories Consumed</p>
            <p className="text-5xl font-bold text-gray-900">1,240</p>
            <p className="text-sm text-gray-400 mt-2">Goal: 2,400 kcal</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <h2 className="text-xl font-semibold mb-4">Recent Meals</h2>
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="font-semibold">Grilled Chicken Salad</p>
              <p className="text-sm text-gray-500">Lunch • 12:30 PM</p>
            </div>
            <p className="font-bold text-green-600">450 kcal</p>
          </div>
        </div>
      </div>
    </div>
  );
};
