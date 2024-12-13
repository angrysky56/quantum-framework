import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, AlertCircle, Activity } from 'lucide-react';

const PredictiveSuggestionsMonitor = () => {
  // Sample metric history and predictions
  const metricHistory = [
    { timestep: 1, coherence: 0.92, stability: 0.95, load: 0.3 },
    { timestep: 2, coherence: 0.90, stability: 0.93, load: 0.4 },
    { timestep: 3, coherence: 0.87, stability: 0.90, load: 0.5 },
    { timestep: 4, coherence: 0.85, stability: 0.87, load: 0.6 },
    { timestep: 5, coherence: 0.83, stability: 0.85, load: 0.7 }
  ];

  const predictions = [
    {
      metric: 'Coherence',
      trend: -0.023,
      confidence: 0.85,
      risk: 'medium'
    },
    {
      metric: 'Stability',
      trend: -0.026,
      confidence: 0.82,
      risk: 'medium'
    },
    {
      metric: 'Load',
      trend: 0.100,
      confidence: 0.90,
      risk: 'high'
    }
  ];

  const getTrendIcon = (trend) => {
    if (trend > 0) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (trend < 0) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Activity className="w-4 h-4 text-gray-500" />;
  };

  const getRiskColor = (risk) => {
    const colors = {
      low: 'bg-green-50 text-green-700 border-green-200',
      medium: 'bg-yellow-50 text-yellow-700 border-yellow-200',
      high: 'bg-red-50 text-red-700 border-red-200'
    };
    return colors[risk] || 'bg-gray-50 text-gray-700 border-gray-200';
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Predictive Analysis Monitor</CardTitle>
          <Activity className="w-6 h-6 text-blue-500" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Metric Trends Chart */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Metric Trends</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={metricHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestep" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="coherence" 
                    stroke="#3b82f6" 
                    name="Coherence"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="stability" 
                    stroke="#22c55e" 
                    name="Stability"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="load" 
                    stroke="#ef4444" 
                    name="Load"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Predictions */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Current Predictions</h3>
            <div className="grid gap-4">
              {predictions.map((prediction) => (
                <div 
                  key={prediction.metric}
                  className={`p-4 rounded-lg border ${getRiskColor(prediction.risk)}`}
                >
                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <div className="font-medium">{prediction.metric}</div>
                      <div className="text-sm">
                        Confidence: {(prediction.confidence * 100).toFixed(1)}%
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getTrendIcon(prediction.trend)}
                      <span className="text-sm font-medium">
                        {prediction.trend > 0 ? '+' : ''}{(prediction.trend * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                  {prediction.risk === 'high' && (
                    <div className="mt-2 text-sm flex items-center space-x-1">
                      <AlertCircle className="w-4 h-4" />
                      <span>Intervention recommended</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PredictiveSuggestionsMonitor;