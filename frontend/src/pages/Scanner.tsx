import { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { useAuth } from '../hooks/useAuth';

export const Scanner = () => {
  const webcamRef = useRef<Webcam>(null);
  const { token } = useAuth();
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const capture = useCallback(async () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (!imageSrc) return;

    setLoading(true);
    try {
      // Convert base64 to blob
      const res = await fetch(imageSrc);
      const blob = await res.blob();
      
      const formData = new FormData();
      formData.append('file', blob, 'food.jpg');

      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/food/analyze`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      
      setAnalysis(response.data);
    } catch (error) {
      console.error('Error analyzing food:', error);
    } finally {
      setLoading(false);
    }
  }, [webcamRef, token]);

  return (
    <div className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Scan Food</h1>
      <div className="rounded-xl overflow-hidden shadow-lg bg-black relative aspect-video mb-4">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={{ facingMode: "environment" }}
          className="w-full h-full object-cover"
        />
      </div>
      <button 
        onClick={capture}
        disabled={loading}
        className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold shadow-md hover:bg-primary-700 disabled:opacity-50"
      >
        {loading ? 'Analyzing...' : 'Scan Now'}
      </button>

      {analysis && (
        <div className="mt-6 bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-bold text-green-600">{analysis.health_score}/10 Health Score</h2>
          <p className="mt-2 text-gray-700">Calories: {analysis.total.calories} kcal</p>
          <div className="mt-4">
            <h3 className="font-semibold">Detected Foods:</h3>
            <ul className="list-disc pl-5 mt-2">
              {analysis.foods.map((food: any, i: number) => (
                <li key={i}>{food.name} ({food.quantity})</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
