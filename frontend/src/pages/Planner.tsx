import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export const Planner = () => {
  const [goals, setGoals] = useState('High protein, low carb, 2000 calories');
  const [plan, setPlan] = useState('');
  const [generating, setGenerating] = useState(false);
  const { token } = useAuth();

  const generatePlan = async () => {
    setGenerating(true);
    setPlan('');
    
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/planner/generate?goals=${encodeURIComponent(goals)}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (!response.body) throw new Error('No readable stream');
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data !== '[DONE]') {
                setPlan(prev => prev + data);
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming error:', error);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">AI Meal Planner</h1>
      
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <label className="block text-sm font-medium text-gray-700 mb-2">Your Goals</label>
        <textarea
          value={goals}
          onChange={(e) => setGoals(e.target.value)}
          className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
          rows={3}
        />
        <button
          onClick={generatePlan}
          disabled={generating}
          className="mt-4 w-full md:w-auto px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
        >
          {generating ? 'Generating Plan...' : 'Generate 7-Day Plan'}
        </button>
      </div>

      {plan && (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-semibold mb-4">Your Generated Plan</h2>
          <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono bg-gray-50 p-4 rounded">{plan}</pre>
        </div>
      )}
    </div>
  );
};
