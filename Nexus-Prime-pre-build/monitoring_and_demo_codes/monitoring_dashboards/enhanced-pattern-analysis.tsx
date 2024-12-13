import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, Activity } from 'lucide-react';

const EnhancedPatternAnalysis = () => {
  // Sample data from our test results
  const stateData = [
    { state: 'healthy_stable', coherence: 0.9000, samples: 1, load: 0.2000 },
    { state: 'moderate_load_stable', coherence: 0.8500, samples: 1, load: 0.3600 },
    { state: 'moderate_load_variable', coherence: 0.8500, samples: 1, load: 0.5200 },
    { state: 'high_load_stressed', coherence: 0.8500, samples: 1, load: 0.6800 },
    { state: 'extreme_load', coherence: 0.8500, samples: 6, load: 0.9500 }
  ];

  const getStateColor = (state) => {
    const colors = {
      healthy_stable: '#22c55e',
      moderate_load_stable: '#84cc16',
      moderate_load_variable: '#eab308',
      high_load_stressed: '#f97316',
      extreme_load: '#ef4444'
    };
    return colors[state] || '#6b7280';
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Enhanced Pattern Analysis</CardTitle>
          <Activity className="w-6 h-6 text-blue-500" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* State Distribution */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">State Distribution</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stateData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="state" 
                    angle={-45} 
                    textAnchor="end" 
                    height={80}
                    interval={0}
                  />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar 
                    dataKey="samples" 
                    fill="#3b82f6" 
                    name="Number of Samples"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Coherence by State */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Coherence & Load Analysis</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={stateData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="state" 
                    angle={-45} 
                    textAnchor="end" 
                    height={80}
                    interval={0}
                  />
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
                    dataKey="load" 
                    stroke="#ef4444" 
                    name="Load"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* State Details */}
          <div className="grid gap-4">
            {stateData.map((state) => (
              <div 
                key={state.state}
                className="p-4 bg-white border rounded-lg"
                style={{ borderLeftWidth: '4px', borderLeftColor: getStateColor(state.state) }}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-medium">{state.state}</div>
                    <div className="text-sm text-gray-500">
                      Samples: {state.samples}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium">
                      Coherence: {(state.coherence * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500">
                      Load: {(state.load * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default EnhancedPatternAnalysis;